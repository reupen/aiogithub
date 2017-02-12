import asyncio
import json
import os.path
import urllib.parse
from collections import OrderedDict

import aiohttp

URLS = {
    '/users/reupen',
    '/users/reupen/repos',
    '/users/reupen/events',
    '/users/reupen/followers',
    '/users/reupen/received_events',
    '/users/reupen/starred',
    '/users/reupen/subscriptions',
    '/repos/reupen/columns_ui',
    '/repos/reupen/columns_ui/assignees',
    '/repos/reupen/columns_ui/commits',
    '/repos/reupen/columns_ui/branches',
    '/repos/reupen/columns_ui/releases',
    '/repos/reupen/columns_ui/stargazers',
}

BASE_URL = 'https://api.github.com'


async def main():
    headers = {'Accept': 'application/vnd.github.v3+json'}
    client = aiohttp.ClientSession(headers=headers)

    with aiohttp.Timeout(10):
        for url in URLS:
            url_parts = urllib.parse.urlsplit(url)

            async with client.get(BASE_URL + url) as response:
                assert response.status == 200
                data = await response.text()
                out_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..', 'mock_data',
                                 url_parts.path[1:] + '.json'))

                os.makedirs(os.path.dirname(out_path), exist_ok=True)

                parsed_data = json.loads(data, object_pairs_hook=OrderedDict)

                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(parsed_data, f, indent=2)

    client.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
