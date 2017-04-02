from typing import AsyncIterator, TypeVar, List, AsyncIterable

import uritemplate
import dateutil.parser

from aiogithub.helpers.typing import is_list_type_hint, get_list_element_hint

T = TypeVar('T')


class BaseObject(dict):
    """Base class for all data objects"""

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
        raise AttributeError(attr)

    def _normalise_document(self, document):
        for key in document:
            value = document[key]

            if key.endswith('_at'):
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
    """Base class for objects where the contained data corresponds to a
    response payload of a particular GitHub API URL
    """
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

    def _get_related_url(self, property_name, element_type, **kwargs):
        if property_name in self:
            template = self[property_name]
            url = uritemplate.expand(template, kwargs)
            return self._client.get_list_absolute_url(
                url, element_type,
                fetch_params=self._get_related_fetch_params()
            )
        else:
            template = self._default_urls[property_name].format(
                **self._fetch_params, **self
            )
            url = uritemplate.expand(template, kwargs)
            return self._client.get_list_relative_url(
                url, element_type,
                fetch_params=self._get_related_fetch_params()
            )

    async def _get_related_object(self, property_name, element_type,
                                  **kwargs):
        if property_name in self:
            template = self[property_name]
            url = uritemplate.expand(template, kwargs)
            response_tuple = await self._client.get_absolute_url(
                url, element_type
            )
        else:
            template = self._default_urls[property_name].format(
                **self._fetch_params
            )
            url = uritemplate.expand(template, kwargs)
            response_tuple = await self._client.get_relative_url(
                url, element_type
            )
        return element_type(self._client, *response_tuple)

    @property
    def limits(self):
        return self._limits


class PaginatedList(AsyncIterator[T]):
    """Internal class used to fetch paginated list data from a particular
    GitHub API endpoint"""

    def __init__(self, client, element_type, initial_document, limits, links,
                 max_items=None, fetch_params=None):
        self._client = client
        self._element_type = element_type
        self._pages = [initial_document]
        self._current_page_number = 0
        self._fetch_params = fetch_params

        self._current_iter = None
        self._current_index = None
        self._limits = BaseObject(limits)
        self._last_raw_limits = limits
        self._max_items = max_items
        self._header_links = links
        self._item_counter = len(initial_document)

    async def __aiter__(self) -> 'PaginatedList[T]':
        self._current_index = 0
        self._current_page_number = 0
        self._current_iter = iter(self._pages[self._current_page_number])
        return self

    async def __anext__(self) -> T:
        if (self._max_items is not None and self._current_index >=
                self._max_items):
            raise StopAsyncIteration
        try:
            value = next(self._current_iter)
            self._current_index += 1
        except StopIteration:
            if self._current_page_number + 1 < len(self._pages):
                self._increment_page_number()
                return await self.__anext__()
            elif self._has_more_pages():
                await self._get_next_page()
                self._increment_page_number()
                return await self.__anext__()
            raise StopAsyncIteration
        return self._make_element(value)

    @property
    def limits(self):
        return self._limits

    def set_max_items(self, max_items):
        self._max_items = max_items

    async def get_all(self) -> List[T]:
        items = []
        for page in self._pages:
            items += map(self._make_element, page)
        while self._has_more_pages():
            await self._get_next_page()
            items += map(self._make_element, self._pages[-1])
        return items[:self._max_items]

    def _has_more_pages(self) -> bool:
        return (self._max_items is None or self._item_counter < self._max_items
                ) and 'next' in self._header_links

    def _make_element(self, document) -> T:
        return self._element_type(self._client, document,
                                  self._last_raw_limits,
                                  fetch_params=self._fetch_params)

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


class PaginatedListProxy(AsyncIterable[T]):
    """Public interface to paginated objects"""

    def __init__(self, client, url, element_type, fetch_params):
        self._client = client
        self._url = url
        self._element_type = element_type
        self._fetch_params = fetch_params
        self._max_items = None
        self._paginator = None

    async def __aiter__(self) -> 'PaginatedList[T]':
        """Asynchronously iterates through all items in the collection.
        Pages are fetched as required.

        Use :func:`~aiogithub.objects.PaginatedListProxy.limit` when listing
        large data sets (e.g. all public users) to avoid making a large
        number of HTTP requests and exhausting your API limits.
        """
        paginator = await self._get_paginator()
        return await paginator.__aiter__()

    def limit(self, max_items):
        """Limits the number of items returned by
        :func:`~aiogithub.objects.PaginatedListProxy.all` or when iterating
        through the collection elements (using `async for`).

        Use when listing large data sets (e.g. all public users) to avoid
        making a large number of HTTP requests and exhausting your API limits.
        """
        self._max_items = max_items
        if self._paginator:
            self._paginator.set_max_items(self._max_items)
        return self

    async def all(self):
        """Returns all items in the collection. This will fetch all
        result pages that haven't already been fetched.

        Use :func:`~aiogithub.objects.PaginatedListProxy.limit` when listing
        large data sets (e.g. all public users) to avoid making a large
        number of HTTP requests and exhausting your API limits.
        """
        paginator = await self._get_paginator()
        return await paginator.get_all()

    async def _get_paginator(self):
        if not self._paginator:
            response_tuple = await self._client.get_absolute_url(self._url,
                                                                 True)
            self._paginator = PaginatedList(self, self._element_type,
                                            *response_tuple,
                                            max_items=self._max_items,
                                            fetch_params=self._fetch_params)
        return self._paginator
