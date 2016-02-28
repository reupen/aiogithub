from collections import UserDict, abc

import dateutil.parser

from ..utils import strip_github_url_params


class BaseObject(UserDict):
    def __init__(self, document):
        # FIXME: separate class for lists
        for key in document:
            if key[-3:] == '_at':
                if isinstance(document[key], str):
                    document[key] = dateutil.parser.parse(document[key])
            elif key in self._get_key_mappings():
                elem_type = self._get_key_mappings()[key]
                if not isinstance(document[key], elem_type):
                    document[key] = elem_type(self._client, document[key],
                                              self._limits)

        super().__init__(document)

    @staticmethod
    def _get_key_mappings():
        return {}

    def __getattr__(self, attr):
        if attr in self:
            return self.get(attr)
        raise AttributeError


class BaseResponseObject(BaseObject):
    def __init__(self, client, document, limits, links=None):
        self._client = client
        self._limits = BaseObject(limits)
        self._links = links

        super().__init__(document)

    async def _get_related_url(self, property_name, element_type):
        url = strip_github_url_params(self[property_name])
        return await self._client.get_list_absolute_url(url, element_type)

    @property
    def limits(self):
        return self._limits


class BaseList(abc.AsyncIterable):
    def __init__(self, client, element_type, initial_document, limits, links,
                 max_items=None):
        self._client = client
        self._element_type = element_type
        self._pages = [initial_document]
        self._current_page_number = 0

        self._current_iter = None
        self._limits = BaseObject(limits)
        self._last_raw_limits = limits
        self._max_items = max_items
        self._links = links
        self._item_counter = len(initial_document)

    @property
    def limits(self):
        return self._limits

    async def get_all(self):
        ret = []
        for page in self._pages:
            ret += page
        while self._item_counter < self._max_items and 'next' in \
                self._links:
            await self._get_next_page()
            ret += self._pages[-1]
        return ret

    async def __aiter__(self):
        self._current_page_number = 0
        self._current_iter = iter(self._pages[self._current_page_number])
        return self

    def _increment_page_number(self):
        self._current_page_number += 1
        self._current_iter = iter(
            self._pages[self._current_page_number]
        )

    async def _get_next_page(self):
        assert 'next' in self._links
        document, limits, links = await self._client.get_absolute_url(
            self._links['next'])
        self._pages.append(document)
        self._last_raw_limits = limits
        self._links = links
        self._item_counter += len(document)

    async def __anext__(self):
        try:
            value = next(self._current_iter)
        except StopIteration:
            if self._current_page_number + 1 < len(self._pages):
                self._increment_page_number()
                return await self.__anext__()
            elif self._item_counter < self._max_items and 'next' in \
                    self._links:
                await self._get_next_page()
                self._increment_page_number()
                return await self.__anext__()
            raise StopAsyncIteration
        return self._element_type(self._client, value, self._last_raw_limits)
