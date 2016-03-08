from pprint import pprint

import asyncio
from aiogithub import GitHub

TOKEN = None

async def main():
    with GitHub(token=TOKEN) as api:
        user = await api.get_user('reupen')
        pprint(user)

        repos = await user.get_repos()
        async for elem in repos:
            pprint(elem.name)

        # Or:
        repos = await user.get_repos()
        all_repos = await repos.get_all()
        pprint([elem.name for elem in all_repos])

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
