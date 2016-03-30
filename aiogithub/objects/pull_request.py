from datetime import datetime

from aiogithub.objects.base_object import BaseResponseObject
from aiogithub.utils import return_key
from aiogithub import objects
from aiogithub.objects.head_base import Head, Base
from aiogithub.objects.user import User


class PullRequest(BaseResponseObject):
    _url = 'repos/{user}/{repo}/pulls/{number}'
    _default_urls = {
        'issue_url': 'repos/{user}/{repo}/issues/{number}',
        'commits_url': 'repos/{user}/{repo}/pulls/{number}/commits',
        'review_comments_url': 'repos/{user}/{repo}/pulls/{number}/comments',
        'review_comment_url': 'repos/{user}/{repo}/pulls/comments/{number}',
        'comments_url': 'repos/{user}/{repo}/issues/{number}/comments'
    }

    @staticmethod
    def _get_key_mappings():
        return {
            'user': objects.User,
            'repo': objects.Repo,
            'assignee': objects.User,
            'milestone': objects.Milestone,
            'head': objects.Head,
            'base': objects.Base
        }

    async def get_issue(self) -> 'objects.Issue':
        return await self._get_related_object('issue_url', objects.Issue)

    async def get_commits(self) -> 'objects.BaseList[objects.Commit]':
        return await self._get_related_url('commits_url', objects.Commit)

    async def get_review_comments(self) \
            -> 'objects.BaseList[objects.ReviewComment]':
        return await self._get_related_url('review_comments_url',
                                           objects.ReviewComment)

    async def get_review_comment(self) -> 'objects.ReviewComment':
        return await self._get_related_object('review_comment_url',
                                              objects.BaseResponseObject)

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
    def diff_url(self) -> str:
        pass

    @property
    @return_key
    def patch_url(self) -> str:
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
    def milestone(self) -> objects.Milestone:
        pass

    @property
    @return_key
    def locked(self) -> bool:
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
    def merged_at(self) -> datetime:
        pass

    @property
    @return_key
    def head(self) -> Head:
        pass

    @property
    @return_key
    def base(self) -> Base:
        pass

    @property
    @return_key
    def user(self) -> User:
        pass

    @property
    @return_key
    def _links(self) -> dict:
        pass
