from collections import UserDict
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
    def __init__(self, document, limits):
        super().__init__(document)

        self._limits = BaseObject(limits)

    @property
    def limits(self):
        return self._limits
