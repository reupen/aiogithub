#!/usr/bin/env python3

from pprint import pprint

import asyncio
from aiogithub import GitHub

TOKEN = None


async def main():
    with GitHub(token=TOKEN) as api:
        user = await api.get_user('reupen')
        pprint(user)

        async for elem in user.get_repos():
            pprint(elem.name)

        # Or:
        all_repos = await user.get_repos().all()
        pprint([elem.name for elem in all_repos])


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
