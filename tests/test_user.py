import dateutil.parser

import pytest

import aiogithub
import aiogithub.objects

from .mocks import fake_response  # noqa


@pytest.mark.asyncio
async def test_get_user():
    with aiogithub.GitHub() as gh:
        user = await gh.get_user('reupen')
    assert user.login == 'reupen'
    assert user.id == 12693549
    assert user.gravatar_id == ''
    assert user.html_url == 'https://github.com/reupen'
    assert user.type == 'User'
    assert user.site_admin is False
    assert user.company is None
    assert user.blog is None
    assert user.location == 'London, UK'
    assert user.email is None
    assert user.hireable is None
    assert user.bio is None
    assert user.public_repos == 13
    assert user.public_gists == 0
    assert user.followers == 1
    assert user.following == 0
    assert user.created_at == dateutil.parser.parse('2015-06-01T09:04:54Z')
    assert user.updated_at == dateutil.parser.parse('2016-03-05T11:37:45Z')

    # Check that refetching works
    await user.fetch_data()


@pytest.mark.asyncio
async def test_get_user_repos():
    with aiogithub.GitHub() as gh:
        user = await gh.get_user('reupen', should_fetch_data=False)
        repos = await user.get_repos()
    assert isinstance(repos, aiogithub.objects.BaseList)
    repo_list = await repos.get_all()
    assert isinstance(repo_list, list)
    assert isinstance(repo_list[0], aiogithub.objects.Repo)
    assert repo_list[0].name == 'album_list_panel'
    assert len(repo_list) == 13
