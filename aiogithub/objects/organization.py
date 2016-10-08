from datetime import datetime

from aiogithub.objects.response import BaseResponseObject
from aiogithub.utils import return_key
from aiogithub import objects


class PartialOrganization(BaseResponseObject):
    _url = 'orgs/{login}'

    _default_urls = {
        'followers_url': 'users/{login}/followers',
        'following_url': 'users/{login}/following{/other_user}',
        'gists_url': 'users/{login}/gists{/gist_id}',
        'repos_url': 'orgs/{login}/repos',
        'events_url': 'orgs/{login}/events',
        'hooks_url': 'orgs/{login}/hooks',
        'issues_url': 'orgs/{login}/issues',
        'members_url': 'orgs/{login}/members{/member}',
        'public_members_url': 'orgs/{login}/public_members{/member}'
    }

    async def get_followers(self) -> 'objects.BaseList[objects.User]':
        return await self._get_related_url('followers_url', objects.User)

    async def get_following(self) -> 'objects.BaseList[objects.User]':
        return await self._get_related_url('following_url', objects.User)

    async def get_gists(self) -> 'objects.BaseList[objects.Gist]':
        return await self._get_related_url('gists_url', objects.Gist)

    async def get_repos(self) -> 'objects.BaseList[objects.Repo]':
        return await self._get_related_url('repos_url', objects.Repo)

    async def get_events(self) -> 'objects.BaseList[objects.Event]':
        return await self._get_related_url('events_url', objects.Event)

    async def get_hooks(self) -> 'objects.BaseList[objects.BaseObject]':
        return await self._get_related_url(
            'hooks_url', objects.BaseObject
        )

    async def get_issues(self) -> 'objects.BaseList[objects.Issue]':
        return await self._get_related_url('issues_url', objects.Issue)

    async def get_members(self) -> 'objects.BaseList[objects.PartialUser]':
        return await self._get_related_url('members_url', objects.PartialUser)

    async def get_public_members(self) -> \
            'objects.BaseList[objects.PartialUser]':
        return await self._get_related_url(
            'public_members_url', objects.PartialUser
        )

    @property
    @return_key
    def login(self) -> str:
        pass

    @property
    @return_key
    def id(self) -> int:
        pass

    @property
    @return_key
    def avatar_url(self) -> str:
        pass

    @property
    @return_key
    def description(self) -> str:
        pass


class Organization(PartialOrganization):
    @property
    @return_key
    def name(self) -> str:
        pass

    @property
    @return_key
    def company(self) -> str:
        pass

    @property
    @return_key
    def blog(self) -> str:
        pass

    @property
    @return_key
    def location(self) -> str:
        pass

    @property
    @return_key
    def email(self) -> str:
        pass

    @property
    @return_key
    def public_repos(self) -> int:
        pass

    @property
    @return_key
    def public_gists(self) -> int:
        pass

    @property
    @return_key
    def followers(self) -> int:
        pass

    @property
    @return_key
    def following(self) -> int:
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

    @property
    @return_key
    def type(self) -> str:
        pass
