from aiogithub import objects
from aiogithub.objects.response import BaseResponseObject
from aiogithub.utils import return_key


class Commit(BaseResponseObject):
    _url = 'repos/{login}/{repo}/commits/{sha}'

    @staticmethod
    def _get_key_mappings():
        return {
            'author': objects.User,
            'committer': objects.User
        }

    async def get_comments(self) -> 'objects.BaseList[objects.Comment]':
        return await self._get_related_url('comments_url', objects.Comment)

    @property
    @return_key
    def sha(self) -> str:
        pass

    @property
    @return_key
    def html_url(self) -> str:
        pass

    @property
    @return_key
    def commit(self) -> dict:  # FIXME: Expose tree as object
        pass

    @property
    @return_key
    def author(self) -> 'objects.User':
        pass

    @property
    @return_key
    def committer(self) -> 'objects.User':
        pass

    @property
    @return_key
    def parents(self) -> list:  # FIXME: make list of Parent objects
        pass

    @property
    @return_key
    def stats(self) -> dict:
        pass

    @property
    @return_key
    def files(self) -> dict:
        pass
