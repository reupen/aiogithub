from .base_object import BaseResponseObject
from .utils import strip_github_url_params
from .repo import Repo


class User(BaseResponseObject):
    async def get_followers(self):
        url = strip_github_url_params(self['followers_url'])
        return await self._client.get_list_absolute_url(url, User)

    async def get_following(self):
        url = strip_github_url_params(self['following_url'])
        return await self._client.get_list_absolute_url(url, User)

    async def get_starred(self):
        url = strip_github_url_params(self['starred_url'])
        return await self._client.get_list_absolute_url(url, Repo)

    async def get_repos(self):
        url = strip_github_url_params(self['repos_url'])
        return await self._client.get_list_absolute_url(url, Repo)

    pass
