import asyncio

import aiohttp
import link_header

from .base_object import BaseList
from .user import User

MAX_ITEMS = 200


class GitHub:
    def __init__(self):
        headers = {'Accept': 'application/vnd.github.v3+json'}
        self.client = aiohttp.ClientSession(headers=headers)
        self.timeout = 10
        self.base_url = 'https://api.github.com'

    async def get_absolute_url(self, url):
        with aiohttp.Timeout(self.timeout):
            async with self.client.get(url) as response:
                limits = {
                    'limit': response.headers.get('X-RateLimit-Limit'),
                    'remaining': response.headers.get('X-RateLimit-Limit')
                }
                link_header_value = response.headers.get('link')
                links_dict = None
                if link_header_value:
                    links = link_header.parse(link_header_value)
                    links_dict = {link.rel: link.href for link in links.links}
                return await response.json(), limits, links_dict

    async def get_url(self, path):
        return await self.get_absolute_url(self.base_url + '/' + path)

    async def get_user(self, user_name):
        return User(*await self.get_url('user/' + user_name))

    async def get_users(self, since=None, max_items=MAX_ITEMS):
        return BaseList(self, User, *await self.get_url('users'),
                        max_items=max_items)

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
