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


class ReviewComment(BaseResponseObject):
    _url = 'repos/{user}/{repo}/pulls/comments/{id}'

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
    def diff_hunk(self) -> str:
        pass

    @property
    @return_key
    def path(self) -> str:
        pass

    @property
    @return_key
    def position(self) -> int:
        pass

    @property
    @return_key
    def original_position(self) -> int:
        pass

    @property
    @return_key
    def commit_id(self) -> str:
        pass

    @property
    @return_key
    def original_commit_id(self) -> str:
        pass

    @property
    @return_key
    def user(self) -> 'objects.User':
        pass

    @property
    @return_key
    def body(self) -> str:
        pass

    @property
    @return_key
    def created_at(self) -> datetime:
        pass

    @property
    @return_key
    def updated_at(self) -> datetime:
        pass

    @property
    @return_key
    def html_url(self) -> str:
        pass

    async def get_pull_request(self) -> 'objects.PullRequest':
        return await self._get_related_object('pull_request_url',
                                              objects.PullRequest)



