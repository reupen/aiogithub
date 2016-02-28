from aiogithub.objects.base_object import BaseResponseObject
from aiogithub.utils import strip_github_url_params

from aiogithub import objects


class User(BaseResponseObject):
    async def get_followers(self):
        return await self._get_related_url('followers_url', objects.User)

    async def get_following(self):
        return await self._get_related_url('following_url', objects.User)

    async def get_starred(self):
        return await self._get_related_url('starred_url', objects.Repo)

    async def get_subscriptions(self):
        return await self._get_related_url('subscriptions_url', objects.Repo)

    async def get_repos(self):
        return await self._get_related_url('repos_url', objects.Repo)

    async def get_events(self):
        return await self._get_related_url('events_url', objects.Event)

    async def get_received_events(self):
        return await self._get_related_url('received_events_url',
                                           objects.Event)
