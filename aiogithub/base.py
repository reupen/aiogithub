import asyncio
import aiohttp

from .user import User


class GitHub:
    def __init__(self):
        headers = {'Accept': 'application/vnd.github.v3+json'}
        self.client = aiohttp.ClientSession(headers=headers)
        self.timeout = 10
        self.base_url = 'https://api.github.com'

    async def get_url(self, path):
        with aiohttp.Timeout(self.timeout):
            async with self.client.get(self.base_url + '/' + path) as response:
                print(response.status)
                print(response.headers)
                limits = {
                    'limit': response.headers.get('X-RateLimit-Limit'),
                    'remaining': response.headers.get('X-RateLimit-Limit')
                }
                return User(await response.json(), limits)

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()