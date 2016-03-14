import pytest

import aiogithub
import aiogithub.objects

from .mocks import fake_response


@pytest.mark.asyncio
async def test_get_user():
    with aiogithub.GitHub() as gh:
        user = await gh.get_user('reupen')
    assert user.login == 'reupen'


@pytest.mark.asyncio
async def test_get_user_repos():
    with aiogithub.GitHub() as gh:
        user = await gh.get_user('reupen')
        repos = await user.get_repos()
    assert isinstance(repos, aiogithub.objects.BaseList)
    repo_list = await repos.get_all()
    assert isinstance(repo_list, list)
    assert isinstance(repo_list[0], aiogithub.objects.Repo)
