import asyncio
import urllib.parse
import os.path

import aiohttp

URLS = {
    '/users/reupen',
    '/users/reupen/repos',
    '/repos/reupen/columns_ui',
    '/repos/reupen/columns_ui/branches'
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
                    os.path.join(os.path.dirname(__file__), '..', 'mocks',
                                 url_parts.path[1:] + '.json'))

                os.makedirs(os.path.dirname(out_path), exist_ok=True)

                with open(out_path, 'w') as f:
                    f.write(data)

    client.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
