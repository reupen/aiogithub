from datetime import datetime

from aiogithub import objects
from aiogithub.objects.base_object import BaseResponseObject
from aiogithub.utils import return_key


class Comment(BaseResponseObject):
    _url = 'repos/{user}/{repo}/issues/comments/{id}'

    @staticmethod
    def _get_key_mappings():
        return {
            'user': objects.User
        }

    @property
    @return_key
    def id(self) -> int:
        pass

    @property
    @return_key
    def html_url(self) -> str:
        pass

    @property
    @return_key
    def body(self) -> str:
        pass

    @property
    @return_key
    def user(self) -> 'objects.User':
        pass

    @property
    @return_key
    def created_at(self) -> datetime:
        pass

    @property
    @return_key
    def updated_at(self) -> datetime:
        pass
