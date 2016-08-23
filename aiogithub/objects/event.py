from datetime import datetime

from aiogithub import objects
from aiogithub.objects.base_object import BaseResponseObject
from aiogithub.utils import return_key


class Event(BaseResponseObject):
    @staticmethod
    def _get_key_mappings():
        return {
            'repo': objects.Repo,
            'actor': objects.User,
            'org': objects.Organization
        }

    @property
    @return_key
    def id(self) -> str:
        pass

    @property
    @return_key
    def type(self) -> str:
        pass

    @property
    @return_key
    def public(self) -> bool:
        pass

    @property
    @return_key
    def payload(self) -> dict:
        pass

    @property
    @return_key
    def repo(self) -> 'objects.Repo':
        pass

    @property
    @return_key
    def actor(self) -> 'objects.User':
        pass

    @property
    def organization(self) -> 'objects.Organization':
        return self['org']

    @property
    @return_key
    def created_at(self) -> datetime:
        pass


class IssueEvent(BaseResponseObject):
    _url = 'repos/{login}/{repo}/issues/events/{id}'

    @staticmethod
    def _get_key_mappings():
        return {
            'repo': objects.Repo,
            'actor': objects.User,
            'issue': objects.Issue
        }

    @property
    @return_key
    def id(self) -> int:
        pass

    @property
    @return_key
    def actor(self) -> 'objects.User':
        pass

    @property
    @return_key
    def event(self) -> str:
        pass

    @property
    @return_key
    def commit_id(self) -> str:
        pass

    @property
    @return_key
    def created_at(self) -> datetime:
        pass

    @property
    @return_key
    def issue(self) -> 'objects.Issue':
        pass
