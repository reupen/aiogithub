from aiogithub.objects.base_object import BaseResponseObject
from aiogithub.utils import strip_github_url_params

from aiogithub import objects


class User(BaseResponseObject):
    _url = 'users/{user}'
    _default_urls = {
        'followers_url': 'users/{login}/followers',
        'following_url': 'users/{login}/following{{/other_user}}',
        'gists_url': 'users/{login}/gists{{/gist_id}}',
        'starred_url': 'users/{login}/starred{{/owner}}{{/repo}}',
        'subscriptions_url': 'users/{login}/subscriptions',
        'organizations_url': 'users/{login}/orgs',
        'repos_url': 'users/{login}/repos',
        'events_url': 'users/{login}/events{{/privacy}}',
        'received_events_url': 'users/{login}/received_events',
    }

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
