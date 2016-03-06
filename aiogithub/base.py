import aiohttp
import link_header

from aiogithub.objects.base_object import BaseList
from aiogithub.objects import (User, Organization, Repo, Event,
                               BaseResponseObject, Branch)


class GitHub:
    def __init__(self, token=None, items_per_page=100, timeout_secs=10,
                 max_paginated_items=200):
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
        if token:
            self._headers['Authorization'] = 'token ' + token

    @property
    def base_url(self):
        return self._base_url

    async def get_absolute_url(self, url, is_paginated=False):
        with aiohttp.Timeout(self._timeout):
            params = {}
            if is_paginated:
                params['per_page'] = self._items_per_page
            async with self._client.get(
                    url, headers=self._headers, params=params) as response:
                limits = {
                    'limit': response.headers.get('X-RateLimit-Limit'),
                    'remaining': response.headers.get('X-RateLimit-Limit')
                }
                link_header_value = response.headers.get('link')
                links_dict = {}
                if link_header_value:
                    links = link_header.parse(link_header_value)
                    links_dict = {link.rel: link.href for link in links.links}
                return await response.json(), limits, links_dict

    async def get_relative_url(self, url, is_paginated=False):
        return await self.get_absolute_url(self._base_url + '/' + url,
                                           is_paginated=is_paginated)

    async def get_url(self, path, is_paginated=False):
        return await self.get_absolute_url(self._base_url + '/' + path,
                                           is_paginated)

    async def get_user(self, user_name, fetch_data=True):
        initial_document = {
            'login': user_name
        }
        return await self.get_object_relative_url(
            User, fetch_data=fetch_data,
            document=initial_document)

    async def get_repo(self, owner_name, repo_name, fetch_data=True):
        initial_document = {
            'name': repo_name,
            'owner': {
                'login': owner_name
            }
        }
        return await self.get_object_relative_url(
            Repo, fetch_data=fetch_data, document=initial_document)

    async def get_current_user(self):
        return User(self, *await self.get_url('user'))

    async def get_users(self, since=None):
        # FIXME: add since support
        return await self.get_list_relative_url('users', User)

    async def get_repos(self, since=None):
        # FIXME: add since support
        return await self.get_list_relative_url('repos', Repo)

    async def get_branch(self, owner_name, repo_name, branch_name):
        path = "repos/{owner}/{repo}/branches/{branch}".format(
            owner=owner_name,
            repo=repo_name,
            branch=branch_name
        )
        return await self.get_object_relative_url(Branch)

    async def get_object_relative_url(self, element_type,
                                      fetch_data=False,
                                      document=None):
        element = element_type(self, document, {})
        if fetch_data:
            await element.fetch_data()
        return element

    async def get_list_relative_url(self, path, element_type):
        return await self.get_list_absolute_url(self._base_url + '/' + path,
                                                element_type)

    async def get_list_absolute_url(self, url, element_type):
        return BaseList(self, element_type,
                        *await self.get_absolute_url(url, True),
                        max_items=self._max_paginated_items)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
