from datetime import datetime
from typing import List

from aiogithub.objects.response import BaseResponseObject
from aiogithub.utils import return_key
from aiogithub import objects
from aiogithub.objects.user import User


class Issue(BaseResponseObject):
    _url = 'repos/{repo[owner][login]}/{repo[name]}/issues/{number}'
    _default_urls = {
        'repository_url': 'repos/{repo[owner][login]}/{repo[name]}',
        'labels_url': 'repos/{repo[owner][login]}/{repo[name]}/issues'
                      '/{number}/labels{{/name}}',
        'comments_url': 'repos/{repo[owner][login]}/{repo[name]}/issues'
                        '/{number}/comments',
        'events_url': 'repos/{repo[owner][login]}/{repo[name]}/issues'
                      '/{number}/events'
    }

    @staticmethod
    def _get_key_mappings():
        return {
            'user': objects.User,
            'repo': objects.Repo,
            'assignee': objects.PartialUser,
            'assignees': List[objects.PartialUser],
            'milestone': objects.Milestone
        }

    async def get_repo(self) -> 'objects.Repo':
        return await self._get_related_object('repository_url', objects.Repo)

    async def get_labels(self) \
            -> 'objects.PaginatedList[objects.BaseResponseObject]':
        return await self._get_related_url('labels_url',
                                           objects.BaseResponseObject)

    async def get_events(self) -> 'objects.PaginatedList[objects.IssueEvent]':
        return await self._get_related_url('events_url', objects.IssueEvent)

    async def get_comments(self) -> 'objects.PaginatedList[objects.Comment]':
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
    def assignee(self) -> objects.PartialUser:
        pass

    @property
    @return_key
    def assignees(self) -> List[objects.PartialUser]:
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
