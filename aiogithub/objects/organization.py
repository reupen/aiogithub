from datetime import datetime

from aiogithub.objects.response import (BaseResponseObject,  # noqa
                                        PaginatedListProxy)
from aiogithub.utils import return_key
from aiogithub import objects


class PartialOrganization(BaseResponseObject):
    _url = 'orgs/{login}'

    _default_urls = {
        'followers_url': 'users/{login}/followers',
        'following_url': 'users/{login}/following({/other_user})',
        'gists_url': 'users/{login}/gists({/gist_id})',
        'repos_url': 'orgs/{login}/repos',
        'events_url': 'orgs/{login}/events',
        'hooks_url': 'orgs/{login}/hooks',
        'issues_url': 'orgs/{login}/issues',
        'members_url': 'orgs/{login}/members{(/member})',
        'public_members_url': 'orgs/{login}/public_members{(/member)}'
    }

    def get_followers(self) -> 'PaginatedListProxy[objects.User]':
        return self._get_related_url('followers_url', objects.User)

    def get_following(self) -> 'PaginatedListProxy[objects.User]':
        return self._get_related_url('following_url', objects.User)

    def get_gists(self) -> 'PaginatedListProxy[objects.Gist]':
        return self._get_related_url('gists_url', objects.Gist)

    def get_repos(self) -> 'PaginatedListProxy[objects.Repo]':
        return self._get_related_url('repos_url', objects.Repo)

    def get_events(self) -> 'PaginatedListProxy[objects.Event]':
        return self._get_related_url('events_url', objects.Event)

    def get_hooks(self) -> 'PaginatedListProxy[objects.BaseObject]':
        return self._get_related_url(
            'hooks_url', objects.BaseObject
        )

    def get_issues(self) -> 'PaginatedListProxy[objects.Issue]':
        return self._get_related_url('issues_url', objects.Issue)

    def get_members(self) -> 'PaginatedListProxy[objects.PartialUser]':
        return self._get_related_url('members_url', objects.PartialUser)

    def get_public_members(self) -> 'PaginatedListProxy[objects.PartialUser]':
        return self._get_related_url(
            'public_members_url', objects.PartialUser
        )

    def _get_related_fetch_params(self):
        return {
            'owner': self._fetch_params
        }

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
