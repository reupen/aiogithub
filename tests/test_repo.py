import dateutil.parser

import pytest

import aiogithub
import aiogithub.objects

from .mocks import fake_response  # noqa


def _check_columns_ui_repo(repo):
    assert isinstance(repo.owner, aiogithub.objects.User)
    assert repo.id == 29824265
    assert repo.owner.login == 'reupen'
    assert repo.full_name == 'reupen/columns_ui'
    assert repo.name == 'columns_ui'
    assert repo.private is False
    assert repo.fork is False
    assert repo.html_url == "https://github.com/reupen/columns_ui"
    assert isinstance(repo.size, int)
    assert isinstance(repo.stargazers_count, int)
    assert isinstance(repo.watchers_count, int)
    assert isinstance(repo.forks, int)
    assert isinstance(repo.open_issues_count, int)
    assert repo.language == 'C++'
    assert repo.has_downloads is True
    assert repo.has_issues is True
    assert repo.has_pages is False
    assert repo.has_wiki is True
    assert repo.created_at == dateutil.parser.parse('2015-01-25T18:05:12Z')
    assert repo.updated_at == dateutil.parser.parse('2017-02-06T17:31:08Z')
    assert repo.pushed_at == dateutil.parser.parse('2017-02-07T20:21:01Z')


@pytest.mark.asyncio
async def test_get_repo():
    with aiogithub.GitHub() as gh:
        repo = await gh.get_repo('reupen', 'columns_ui')
    _check_columns_ui_repo(repo)


@pytest.mark.asyncio
async def test_get_repo_defer():
    with aiogithub.GitHub() as gh:
        repo = await gh.get_repo('reupen', 'columns_ui', defer_fetch=True)

    await repo.fetch_data()
    _check_columns_ui_repo(repo)


@pytest.mark.asyncio
async def test_get_repo_refetch():
    with aiogithub.GitHub() as gh:
        repo = await gh.get_repo('reupen', 'columns_ui')

    await repo.fetch_data()
    _check_columns_ui_repo(repo)


@pytest.mark.asyncio
async def test_get_repo_branches():
    with aiogithub.GitHub() as gh:
        repo = await gh.get_repo('reupen', 'columns_ui')
    branches_list = await repo.get_branches().all()
    assert isinstance(branches_list[0], aiogithub.objects.Branch)


@pytest.mark.asyncio
async def test_get_repo_branches_defer():
    with aiogithub.GitHub() as gh:
        repo = await gh.get_repo('reupen', 'columns_ui', defer_fetch=True)
    branches_list = await repo.get_branches().all()
    assert isinstance(branches_list[0], aiogithub.objects.Branch)
