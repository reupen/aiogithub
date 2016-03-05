# aiogithub

asyncio- and aiohttp-based Python 3.5 GitHub API client

## A simple example

```python
import asyncio
from aiogithub import GitHub

TOKEN = None  # Set this to your OAuth token

async def main():
    with GitHub(TOKEN) as api:
        user = await api.get_user('reupen')
        print(user['login'])
        # print(user.login) also works

        # Get this user's repos
        repos = await user.get_repos()
        # There's no need to worry about pagination
        # Simply iterate over list objects like this and pages will be retrieved as needed:
        async for repo in repos:
            pass # Do something with each repo here

        # Or you can fetch the entire list like this:
        repos = await user.get_repos()
        all_repos = await repos.get_all()
        # Do something with all_repos 

asyncio.get_event_loop().run_until_complete(main())
```