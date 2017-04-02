import os
from typing import Optional

import aiohttp
import link_header

import aiogithub
from aiogithub import objects
from aiogithub.objects import response
from aiogithub.exceptions import HttpException

GITHUB_DEFAULT_CONTENT_TYPE = 'application/vnd.github.v3+json'
GITHUB_PREVIEW_CONTENT_TYPE = 'application/vnd.github.black-cat-preview+json'


class GitHub:
    def __init__(self, token: str = None, items_per_page=100, timeout_secs=10,
                 max_paginated_items=1000, enable_preview_api=False):
        """
        Initialises a GitHub API client.

        If no personal access token is provided, the client will check the
        GITHUB_TOKEN environment variable for a token and use that if
        present. If still without a token, the GitHub API will be used
        unauthenticated.

        :param token:                 GitHub personal access token
        :param items_per_page:        Items to request per page, must be
                                      between 1 and 100
        :param timeout_secs:          Timeout in seconds for HTTP requests
        :param max_paginated_items:   Safety limit for when iterating
                                      through list results to avoid
                                      inadvertently making a huge number of
                                      requests

        """
        if not token:
            token = os.environ.get('GITHUB_TOKEN')

        content_type = GITHUB_PREVIEW_CONTENT_TYPE if enable_preview_api \
            else GITHUB_DEFAULT_CONTENT_TYPE

        headers = {
            'Accept': content_type,
            'User-Agent': 'aiogithub/{}'.format(aiogithub.__version__)
        }
        if token:
            headers['Authorization'] = 'token ' + token
        self._client = aiohttp.ClientSession(headers=headers)
        self._timeout = timeout_secs
        self._base_url = 'https://api.github.com'
        self._token = token
        self._items_per_page = items_per_page
        self._max_paginated_items = max_paginated_items
        self._last_limits = None

    @property
    def last_rate_limit(self) -> Optional[dict]:
        """
        The rate limits that were sent by GitHub in the most recent
        request.

        :type: Optional[dict]
        """
        return self._last_limits

    async def get_user(self, username, defer_fetch=False) -> objects.User:
        """
        Gets a single user.

        :param username:    The name of the user to fetch the details of.
        :param defer_fetch: Whether to defer fetching of data about this user.
        :return:            An object representing the user.
        """
        fetch_params = {
            'login': username
        }
        return await self._get_object_relative_url(
            objects.User, defer_fetch=defer_fetch,
            fetch_params=fetch_params)

    async def get_organization(self, username, defer_fetch=False) -> \
            objects.Organization:
        """
        Gets a single organization.

        :param username:    The username/login of the organization to fetch the
                            details of.
        :param defer_fetch: Whether to defer fetching of data about this
                            organization.
        :return:            An object representing the organization.
        """
        fetch_params = {
            'login': username
        }
        return await self._get_object_relative_url(
            objects.Organization, defer_fetch=defer_fetch,
            fetch_params=fetch_params)

    async def get_repo(self, owner_name, repo_name,
                       defer_fetch=False) -> objects.Repo:
        """
        Gets a single repository.

        :param owner_name:  The name of the user or organisation that owns
                            the repository.
        :param repo_name:   The name of the repository.
        :param defer_fetch: Whether to defer fetching of data about this
                            repository.
        :return:            An object representing the repository.
        """
        fetch_params = {
            'name': repo_name,
            'owner': {
                'login': owner_name
            }
        }
        return await self._get_object_relative_url(
            objects.Repo, defer_fetch=defer_fetch,
            fetch_params=fetch_params)

    async def get_branch(self, owner_name, repo_name,
                         branch_name) -> objects.Branch:
        """
        Gets a single branch of a repository.
        """
        fetch_params = {
            'login': owner_name,
            'repo': repo_name,
            'branch': branch_name
        }
        return await self._get_object_relative_url(objects.Branch,
                                                   fetch_params=fetch_params)

    async def get_issue(self, owner_name, repo_name,
                        issue_number) -> objects.Issue:
        """
        Gets a single issue of a repository.
        """
        fetch_params = {
            'login': owner_name,
            'repo': repo_name,
            'number': issue_number
        }
        return await self._get_object_relative_url(objects.Issue,
                                                   fetch_params=fetch_params)

    async def get_pull_request(self, owner_name, repo_name,
                               issue_number) -> objects.PullRequest:
        """
        Gets a single pull request of a repository.
        """
        fetch_params = {
            'login': owner_name,
            'repo': repo_name,
            'number': issue_number
        }
        return await self._get_object_relative_url(objects.PullRequest,
                                                   fetch_params=fetch_params)

    async def get_rate_limit(self) -> objects.RateLimit:
        """
        Gets the current rate limit values.
        """
        return await self._get_object_relative_url(objects.RateLimit)

    async def get_current_user(self) -> objects.AuthenticatedUser:
        """
        Gets the current authenticated user.
        """
        return objects.AuthenticatedUser(
            self, *await self.get_relative_url('user')
        )

    def get_users(self, since=None) -> \
            objects.PaginatedListProxy[objects.User]:
        """
        Gets all users.
        """
        # FIXME: add since support
        return self.get_list_relative_url('users', objects.User)

    def get_repos(self, since=None) -> \
            objects.PaginatedListProxy[objects.Repo]:
        """
        Gets all repos.
        """
        # FIXME: add since support
        return self.get_list_relative_url('repos', objects.Repo)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> 'GitHub':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    async def get_absolute_url(self, url, is_paginated=False) -> tuple:
        with aiohttp.Timeout(self._timeout):
            params = {}
            if is_paginated:
                params['per_page'] = self._items_per_page
            async with self._client.get(
                    url, params=params) as response:
                if response.status >= 400:
                    raise HttpException(response.status, url)
                self._last_limits = {
                    'limit': response.headers.get('X-RateLimit-Limit'),
                    'remaining': response.headers.get('X-RateLimit-Limit')
                }
                link_header_value = response.headers.get('link')
                links_dict = {}
                if link_header_value:
                    links = link_header.parse(link_header_value)
                    links_dict = {link.rel: link.href for link in links.links}
                return await response.json(), self._last_limits, links_dict

    async def get_relative_url(self, url, is_paginated=False) -> tuple:
        return await self.get_absolute_url(self._base_url + '/' + url,
                                           is_paginated=is_paginated)

    async def get_url(self, url: str, relative: bool, is_paginated=False) -> \
            tuple:
        if relative:
            return await self.get_relative_url(url, is_paginated)
        else:
            return await self.get_absolute_url(url, is_paginated)

    def get_list_relative_url(self, path, element_type,
                              fetch_params=None):
        return self.get_list_absolute_url(self._base_url + '/' + path,
                                          element_type,
                                          fetch_params=fetch_params)

    def get_list_absolute_url(self, url, element_type,
                              fetch_params=None):
        return response.PaginatedListProxy(
            self, url, element_type, fetch_params
        )

    async def _get_object_relative_url(self, element_type,
                                       defer_fetch=False,
                                       fetch_params=None):
        element = element_type(self, fetch_params=fetch_params)
        if not defer_fetch:
            await element.fetch_data()
        return element
