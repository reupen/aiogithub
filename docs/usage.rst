.. currentmodule:: aiogithub

Usage
=====

Development status
------------------
This library is a work in progress. So far, select read operations have been implemented.

A note about asyncio
--------------------

aiogithub is written on top of asyncio and aiohttp. You should have a basic grasp of asynchronous programming using
asyncio in Python 3 before using this library.

In particular, using of the library generally occurs in an ``async def`` function. Calls to coroutine functions would normally
be preceded with ``await``, and ``async for`` would normally be used with asynchronous iterables.

A simple example
----------------
::

    import asyncio

    from aiogithub import GitHub

    async def main():
        with GitHub() as api:
            user = await api.get_user('reupen')
            print(user.login)
            # user is also a dict, so you can see the underlying data via print(user)

            # Get this user's repos. There's no need to worry about
            # pagination – you can simply iterate over list objects like
            # this and pages will be retrieved as needed:
            async for repo in user.get_repos():
                pass # Do something with each repo here

            # Or you can fetch the entire list like this:
            repos = await user.get_repos().all()
            # Do something with repos

    asyncio.get_event_loop().run_until_complete(main())


The GitHub class
----------------

The :class:`GitHub` class is the main entry point into aiogithub functionality. It is a wrapper around an aiohttp ClientSession object, which means that
you automatically benefit from connection pooling. You should use the object as a context manager to make sure the session is closed as soon
as you are done with it.

Authentication
--------------

You can make a limited number of requests to the GitHub API unauthenticated, but for most purposes you will want to be authenticated. To authenticate
with GitHub using aiogithub, you should use a personal access token. You can generate a personal access token in `your GitHub settings <https://github.com/settings/tokens>`_.

aiogithub will use the value of the the GITHUB_TOKEN environment variable to authenticate with GitHub if it is set. You can also pass a token to :class:`GitHub` (which will
override any value in the GITHUB_TOKEN environment variable):::

   with GitHub(token='a_personal_access_token') as api:
       pass

