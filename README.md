# aiogithub

[![Build Status](https://travis-ci.org/reupen/aiogithub.svg?branch=master)](https://travis-ci.org/reupen/aiogithub)

asyncio- and aiohttp-based Python 3.5 GitHub API client.

Note: This library is a work in progress. So far, select read operations have been implemented.

## A simple example

```python
import asyncio
from aiogithub import GitHub

TOKEN = None  # Set this a personal access token (or leave as None to 
              # use the API unauthenticated) 

async def main():
    with GitHub(TOKEN) as api:
        user = await api.get_user('reupen')
        print(user.login)
        # user is also a dict, so you can see the underlying data via print(user) 

        # Get this user's repos
        repos = await user.get_repos()
        # There's no need to worry about pagination – you can simply iterate 
        # over list objects like this and pages will be retrieved as needed:
        async for repo in repos:
            pass # Do something with each repo here

        # Or you can fetch the entire list like this:
        repos = await user.get_repos()
        all_repos = await repos.get_all()
        # Do something with all_repos 

asyncio.get_event_loop().run_until_complete(main())
```