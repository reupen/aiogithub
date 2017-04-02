# aiogithub

[![Build Status](https://travis-ci.org/reupen/aiogithub.svg?branch=master)](https://travis-ci.org/reupen/aiogithub) [![Requirements Status](https://requires.io/github/reupen/aiogithub/requirements.svg?branch=master)](https://requires.io/github/reupen/aiogithub/requirements/?branch=master) [![Documentation Status](https://readthedocs.org/projects/aiogithub/badge/?version=latest)](http://aiogithub.readthedocs.io/en/latest/?badge=latest)

asyncio- and aiohttp-based Python 3.5 GitHub API client.

Note: This library is a work in progress. So far, select read operations have been implemented.

## A simple example

```python
import asyncio

from aiogithub import GitHub

# To use the GitHub API authenticated, you can either set the 
# GITHUB_TOKEN environment variable with a personal access token 
# as the value, or explicitly set the token here. Leave as None to 
# use the API unauthenticated. 
TOKEN = None

async def main():
    with GitHub(TOKEN) as api:
        user = await api.get_user('reupen')
        print(user.login)
        # user is also a dict, so you can see the underlying data via
        # print(user)

        # Get this user's repos. There's no need to worry about
        # pagination – you can simply iterate over list objects like
        # this and pages will be retrieved as needed:
        async for repo in user.get_repos():
            pass # Do something with each repo here

        # Or you can fetch the entire list like this:
        repos = user.get_repos().all()
        # Do something with repos

asyncio.get_event_loop().run_until_complete(main())
```

## Installation

Currently, only development versions are available. You can install the current development version by running:

```
pip3.5 install -U setuptools
pip3.5 install git+https://github.com/reupen/aiogithub.git#egg=aiogithub
```