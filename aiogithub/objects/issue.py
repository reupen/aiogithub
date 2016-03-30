from datetime import datetime

from aiogithub.objects.base_object import BaseResponseObject
from aiogithub.utils import return_key
from aiogithub import objects
from aiogithub.objects.user import User


class Issue(BaseResponseObject):
    _url = 'repos/{user}/{repo}/issues/{number}'
    _default_urls = {
        'repository_url': 'repos/{user}/{repo}',
        'labels_url': 'repos/{user}/{repo}/issues/{number}/labels{/name}',
        'comments_url': 'repos/{user}/{repo}/issues/{number}/comments',
        'events_url': 'repos/{user}/{repo}/issues/{number}/events'
    }

    @staticmethod
    def _get_key_mappings():
        return {
            'user': objects.User,
            'repo': objects.Repo,
            'assignee': objects.User,
            'milestone': objects.Milestone
        }

    async def get_repo(self) -> 'objects.BaseList[objects.Repo]':
        return await self._get_related_object('repository_url', objects.Repo)

    async def get_labels(self) \
            -> 'objects.BaseList[objects.BaseResponseObject]':
        return await self._get_related_url('labels_url',
                                           objects.BaseResponseObject)

    async def get_events(self) -> 'objects.BaseList[objects.IssueEvent]':
        return await self._get_related_url('events_url', objects.IssueEvent)

    async def get_comments(self) -> 'objects.BaseList[objects.Comment]':
        return await self._get_related_url('comments_url', objects.Comment)

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
    def number(self) -> int:
        pass

    @property
    @return_key
    def state(self) -> str:
        pass

    @property
    @return_key
    def title(self) -> str:
        pass

    @property
    @return_key
    def body(self) -> str:
        pass

    @property
    @return_key
    def assignee(self) -> objects.User:
        pass

    @property
    @return_key
    def labels(self) -> list:
        pass

    @property
    @return_key
    def milestone(self) -> objects.Milestone:
        pass

    @property
    @return_key
    def locked(self) -> bool:
        pass

    @property
    @return_key
    def comments(self) -> int:
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
    def closed_at(self) -> datetime:
        pass

    @property
    @return_key
    def user(self) -> User:
        pass
