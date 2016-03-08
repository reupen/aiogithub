import aiohttp
import link_header

from aiogithub import objects
from aiogithub.exceptions import HttpException


class GitHub:
    def __init__(self, token=None, items_per_page=100, timeout_secs=10,
                 max_paginated_items=1000):
        """
        :param token:                 GitHub personal access token
        :param items_per_page:        Items to request per page, must be
                                      between 1 and 100
        :param max_paginated_items:   Safety limit for when iterating
                                      through list results to avoid
                                      inadvertently making a huge number of
                                      requests

        """
        headers = {'Accept': 'application/vnd.github.v3+json'}
        self._client = aiohttp.ClientSession(headers=headers)
        self._timeout = timeout_secs
        self._base_url = 'https://api.github.com'
        self._token = token
        self._items_per_page = items_per_page
        self._max_paginated_items = max_paginated_items
        self._headers = {
            'User-Agent': 'aiogithub'
        }
        self._last_limits = None
        if token:
            self._headers['Authorization'] = 'token ' + token

    def get_last_rate_limit(self) -> dict:
        return self._last_limits

    async def get_absolute_url(self, url, is_paginated=False) -> tuple:
        with aiohttp.Timeout(self._timeout):
            params = {}
            if is_paginated:
                params['per_page'] = self._items_per_page
            async with self._client.get(
                    url, headers=self._headers, params=params) as response:
                if response.status >= 400:
                    raise HttpException(response.status)
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

    async def get_url(self, path, is_paginated=False) -> tuple:
        return await self.get_absolute_url(self._base_url + '/' + path,
                                           is_paginated)

    async def get_object_relative_url(self, element_type,
                                      should_fetch_data=True,
                                      fetch_params=None):
        element = element_type(self, fetch_params=fetch_params)
        if should_fetch_data:
            await element.fetch_data()
        return element

    async def get_list_relative_url(self, path, element_type):
        return await self.get_list_absolute_url(self._base_url + '/' + path,
                                                element_type)

    async def get_list_absolute_url(self, url, element_type):
        return objects.BaseList(self, element_type,
                                *await self.get_absolute_url(url, True),
                                max_items=self._max_paginated_items)

    async def get_user(self, user_name,
                       should_fetch_data=True) -> objects.User:
        """
        Gets a single user.
        """
        fetch_params = {
            'user': user_name
        }
        return await self.get_object_relative_url(
            objects.AuthenticatedUser, should_fetch_data=should_fetch_data,
            fetch_params=fetch_params)

    async def get_repo(self, owner_name, repo_name,
                       should_fetch_data=True) -> objects.Repo:
        """
        Gets a single repository.
        """
        fetch_params = {
            'name': repo_name,
            'user': owner_name
        }
        return await self.get_object_relative_url(
            objects.Repo, should_fetch_data=should_fetch_data,
            fetch_params=fetch_params)

    async def get_branch(self, owner_name, repo_name,
                         branch_name) -> objects.Branch:
        """
        Gets a single branch of a repository.
        """
        fetch_params = {
            'user': owner_name,
            'repo': repo_name,
            'branch': branch_name
        }
        return await self.get_object_relative_url(objects.Branch,
                                                  fetch_params=fetch_params)

    async def get_issue(self, owner_name, repo_name,
                        issue_number) -> objects.Issue:
        """
        Gets a single issue of a repository.
        """
        fetch_params = {
            'user': owner_name,
            'repo': repo_name,
            'number': issue_number
        }
        return await self.get_object_relative_url(objects.Issue,
                                                  fetch_params=fetch_params)

    async def get_pull_request(self, owner_name, repo_name,
                               issue_number) -> objects.PullRequest:
        """
        Gets a single pull request of a repository.
        """
        fetch_params = {
            'user': owner_name,
            'repo': repo_name,
            'number': issue_number
        }
        return await self.get_object_relative_url(objects.PullRequest,
                                                  fetch_params=fetch_params)

    async def get_rate_limit(self) -> objects.RateLimit:
        """
        Gets the current rate limit values.
        """
        return await self.get_object_relative_url(objects.RateLimit)

    async def get_current_user(self) -> objects.AuthenticatedUser:
        """
        Gets the current authenticated user.
        """
        return objects.User(self, *await self.get_url('user'))

    async def get_users(self, since=None):
        """
        Gets all users.
        """
        # FIXME: add since support
        return await self.get_list_relative_url('users', objects.User)

    async def get_repos(self, since=None):
        """
        Gets all repos.
        """
        # FIXME: add since support
        return await self.get_list_relative_url('repos', objects.Repo)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
