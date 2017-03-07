from typing import Optional

from aiogithub.objects.response import BaseResponseObject
from aiogithub import objects
from aiogithub.utils import return_key


class Review(BaseResponseObject):
    _url = ('repos/{pull_request[repo][owner][login]}'
            '/{pull_request[repo][name]}/pulls/{pull_request[number]}'
            '/reviews/{id}')
    _default_urls = {
        'pull_request_url': 'repos/{pull_request[repo][owner][login]}'
                            '/{pull_request[repo][name]}/pulls'
                            '/{pull_request[number]}',
        'comments_url': _url + '/comments'
    }

    @staticmethod
    def _get_key_mappings():
        return {
            'user': objects.PartialUser
        }

    async def get_pull_request(self) -> 'objects.PullRequest':
        return await self._get_related_url('pull_request_url',
                                           objects.PullRequest)

    @property
    @return_key
    def id(self) -> Optional[int]:
        """
        :type: int
        """

    @property
    @return_key
    def user(self) -> objects.PartialUser:
        """
        :type: objects.PartialUser
        """

    @property
    @return_key
    def body(self) -> Optional[str]:
        """
        :type: Optional[str]
        """

    @property
    @return_key
    def commit_id(self) -> Optional[str]:
        """
        :type: Optional[str]
        """

    @property
    @return_key
    def state(self) -> Optional[str]:
        """
        :type: Optional[str]
        """

    @property
    @return_key
    def html_url(self) -> Optional[str]:
        """
        :type: Optional[str]
        """

    @property
    @return_key
    def _links(self) -> dict:
        """
        :type: Optional[dict]
        """
