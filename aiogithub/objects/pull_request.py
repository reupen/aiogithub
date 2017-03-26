from datetime import datetime
from typing import List

from aiogithub.objects.response import (BaseResponseObject,  # noqa
                                        PaginatedListProxy)
from aiogithub.utils import return_key
from aiogithub import objects
from aiogithub.objects.head_base import Head, Base
from aiogithub.objects.user import PartialUser


class PullRequest(BaseResponseObject):
    _url = 'repos/{repo[owner][login]}/{repo[name]}/pulls/{number}'
    _default_urls = {
        'issue_url': 'repos/{repo[owner][login]}/{repo[name]}/issues/{number}',
        'commits_url': 'repos/{repo[owner][login]}/{repo[name]}'
                       '/pulls/{number}/commits',
        'requested_reviewers_url': 'repos/{repo[owner][login]}/{repo[name]}'
                                   '/pulls/{number}/requested_reviewers',
        'reviews_url': 'repos/{repo[owner][login]}/{repo[name]}'
                       '/pulls/{number}/reviews',
        'review_comments_url': 'repos/{repo[owner][login]}/{repo[name]}'
                               '/pulls/{number}/comments',
        'review_comment_url': 'repos/{repo[owner][login]}/{repo[name]}'
                              '/pulls/comments/{number}',
        'comments_url': 'repos/{repo[owner][login]}/{repo[name]}'
                        '/issues/{number}/comments'
    }

    @staticmethod
    def _get_key_mappings():
        return {
            'user': objects.PartialUser,
            'repo': objects.Repo,
            'assignee': objects.User,
            'assignees': List[objects.PartialUser],
            'requested_reviewers': List[objects.PartialUser],
            'milestone': objects.Milestone,
            'head': objects.Head,
            'base': objects.Base
        }

    async def get_issue(self) -> 'objects.Issue':
        return await self._get_related_object('issue_url', objects.Issue)

    def get_commits(self) -> 'PaginatedListProxy[objects.Commit]':
        return self._get_related_url('commits_url', objects.Commit)

    def get_requested_reviewers(self) \
            -> 'PaginatedListProxy[objects.PartialUser]':
        return self._get_related_url('requested_reviewers_url',
                                     objects.PartialUser)

    def get_review_comments(self) -> \
            'PaginatedListProxy[objects.ReviewComment]':
        return self._get_related_url('review_comments_url',
                                     objects.ReviewComment)

    def get_reviews(self) -> 'PaginatedListProxy[objects.Review]':
        return self._get_related_url('reviews_url', objects.Review)

    async def get_review_comment(self) -> 'objects.ReviewComment':
        return await self._get_related_object('review_comment_url',
                                              objects.BaseResponseObject)

    def get_comments(self) -> 'PaginatedListProxy[objects.Comment]':
        return self._get_related_url('comments_url', objects.Comment)

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
    def requested_reviewers(self) -> List[objects.PartialUser]:
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
    def user(self) -> PartialUser:
        pass

    @property
    @return_key
    def _links(self) -> dict:
        pass

    def _get_related_fetch_params(self):
        return {
            'pull_request': self._fetch_params
        }
