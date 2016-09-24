from aiogithub.objects.response import BaseResponseObject
from aiogithub.utils import return_key
from aiogithub import objects


class HeadBase(BaseResponseObject):
    @staticmethod
    def _get_key_mappings():
        return {
            'user': objects.User,
            'repo': objects.Repo
        }

    @property
    @return_key
    def label(self) -> str:
        pass

    @property
    @return_key
    def ref(self) -> str:
        pass

    @property
    @return_key
    def sha(self) -> str:
        pass

    pass


class Head(HeadBase):
    pass


class Base(HeadBase):
    pass
