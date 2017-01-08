from collections import abc
from typing import AsyncIterator, TypeVar, List, GenericMeta

import uritemplate
import dateutil.parser

from aiogithub.helpers.typing import is_list_type_hint, get_list_element_hint

T = TypeVar('T')


class BaseObject(dict):
    @staticmethod
    def _get_key_mappings():
        return {}

    def __init__(self, document):
        if document is None:
            document = {}
        super().__init__(self._normalise_document(document))

    def __getattr__(self, attr):
        if attr in self:
            return self.get(attr)
        raise AttributeError

    def _normalise_document(self, document):
        for key in document:
            value = document[key]

            if key[-3:] == '_at':
                if isinstance(value, str):
                    document[key] = dateutil.parser.parse(value)
            elif key in self._get_key_mappings():
                elem_type = self._get_key_mappings()[key]
                if is_list_type_hint(elem_type):
                    elem_subtype = get_list_element_hint(elem_type)
                    for n, sub_elem in enumerate(value):
                        if not isinstance(sub_elem, elem_subtype):
                            document[key][n] = elem_subtype(
                                self._client, sub_elem, self._limits
                            )

                elif not isinstance(document[key], elem_type):
                    document[key] = elem_type(self._client, value,
                                              self._limits)
            else:
                self._normalise_key(document, key)

        return document

    def _normalise_key(self, document, key):
        pass

    def _set_from_document(self, document):
        self.clear()
        self.update(self._normalise_document(document))


class BaseResponseObject(BaseObject):
    _url = None
    _default_urls = {}

    def __init__(self, client, document=None, limits=None, links=None,
                 fetch_params=None):
        self._client = client
        self._limits = BaseObject(limits) if limits is not None else None
        self._header_links = links
        self._fetch_params = fetch_params if fetch_params is not None else {}

        # Called here for now as needs self._client
        super().__init__(document)

    async def fetch_data(self):
        relative = False
        if 'url' in self:
            url = self['url']
        elif '_links' in self and 'self' in self['_links']:
            url = self['_links']['self']
        else:
            relative = True
            url = self._url.format(**self._fetch_params)
            # FIXME: catch appropriate exception
            # raise Exception("No known fetch URL for this object")
        document, limits, links = await self._client.get_url(url, relative)
        self._set_from_document(document)
        self._limits = BaseObject(limits)
        self._header_links = links

    def _get_related_fetch_params(self):
        return None

    async def _get_related_url(self, property_name, element_type, **kwargs):
        if property_name in self:
            template = self[property_name]
            url = uritemplate.expand(template, kwargs)
            return await self._client.get_list_absolute_url(
                url, element_type,
                fetch_params=self._get_related_fetch_params()
            )
        else:
            template = self._default_urls[property_name].format(
                **self._fetch_params, **self
            )
            url = uritemplate.expand(template, kwargs)
            return await self._client.get_list_relative_url(
                url, element_type,
                fetch_params=self._get_related_fetch_params()
            )

    async def _get_related_object(self, property_name, element_type,
                                  **kwargs):
        if property_name in self:
            template = self[property_name]
            url = uritemplate.expand(template, kwargs)
            return await self._client.get_absolute_url(url, element_type)
        else:
            template = self._default_urls[property_name].format(
                **self._fetch_params
            )
            url = uritemplate.expand(template, kwargs)
            return await self._client.get_relative_url(url, element_type)

    @property
    def limits(self):
        return self._limits


class BaseList(AsyncIterator[T], abc.AsyncIterator):
    def __init__(self, client, element_type, initial_document, limits, links,
                 max_items=None, fetch_params=None):
        self._client = client
        self._element_type = element_type
        self._pages = [initial_document]
        self._current_page_number = 0
        self._fetch_params = fetch_params

        self._current_iter = None
        self._limits = BaseObject(limits)
        self._last_raw_limits = limits
        self._max_items = max_items
        self._header_links = links
        self._item_counter = len(initial_document)

    @property
    def limits(self):
        return self._limits

    def _make_element(self, document) -> T:
        return self._element_type(self._client, document,
                                  self._last_raw_limits,
                                  fetch_params=self._fetch_params)

    async def get_all(self) -> List[T]:
        ret = []
        for page in self._pages:
            ret += map(self._make_element, page)
        while self._item_counter < self._max_items and 'next' in \
                self._header_links:
            await self._get_next_page()
            ret += map(self._make_element, self._pages[-1])
        return ret

    async def __aiter__(self) -> 'BaseList[T]':
        self._current_page_number = 0
        self._current_iter = iter(self._pages[self._current_page_number])
        return self

    def _increment_page_number(self) -> None:
        self._current_page_number += 1
        self._current_iter = iter(
            self._pages[self._current_page_number]
        )

    async def _get_next_page(self) -> None:
        assert 'next' in self._header_links
        document, limits, links = await self._client.get_absolute_url(
            self._header_links['next']
        )
        self._pages.append(document)
        self._last_raw_limits = limits
        self._header_links = links
        self._item_counter += len(document)

    async def __anext__(self) -> T:
        try:
            value = next(self._current_iter)
        except StopIteration:
            if self._current_page_number + 1 < len(self._pages):
                self._increment_page_number()
                return await self.__anext__()
            elif self._item_counter < self._max_items and 'next' in \
                    self._header_links:
                await self._get_next_page()
                self._increment_page_number()
                return await self.__anext__()
            raise StopAsyncIteration
        return self._make_element(value)
