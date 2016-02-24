from collections import UserDict, abc

import dateutil.parser


class BaseObject(UserDict):
    def __init__(self, document):
        # FIXME: separate class for lists
        for key in document:
            if key[-3:] == '_at':
                document[key] = dateutil.parser.parse(document[key])

        super().__init__(document)

    def __getattr__(self, attr):
        return self.get(attr)


class BaseResponseObject(BaseObject):
    def __init__(self, document, limits, links=None):
        super().__init__(document)

        self._limits = BaseObject(limits)
        self._links = links

    @property
    def limits(self):
        return self._limits


class BaseList(abc.AsyncIterable):
    def __init__(self, client, element_type, initial_document, limits, links,
                 max_items=None):
        self._client = client
        self._element_type = element_type
        self._current_list = initial_document
        self._current_iter = None
        self._limits = BaseObject(limits)
        self._last_raw_limits = limits
        self._max_items = max_items
        self._links = links
        self._item_counter = len(initial_document)

    @property
    def limits(self):
        return self._limits

    async def __aiter__(self):
        self._current_iter = iter(self._current_list)
        return self

    async def __anext__(self):
        try:
            value = next(self._current_iter)
        except StopIteration:
            if self._item_counter < self._max_items and 'next' in self._links:
                document, limits, links = await self._client.get_absolute_url(
                    self._links['next'])
                self._current_list = document
                self._last_raw_limits = limits
                self._links = links
                self._item_counter += len(document)
                self._current_iter = iter(self._current_list)
                return await self.__anext__()
            raise StopAsyncIteration
        return self._element_type(value, self._last_raw_limits)
