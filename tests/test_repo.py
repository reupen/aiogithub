import dateutil.parser
from copy import deepcopy

import pytest

import aiogithub
import aiogithub.objects

from .mocks import fake_response  # noqa


@pytest.mark.asyncio
async def test_get_repo():
    with aiogithub.GitHub() as gh:
        repo = await gh.get_repo('reupen', 'columns_ui')
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
    assert repo.updated_at == dateutil.parser.parse('2016-03-04T18:24:42Z')
    assert repo.pushed_at == dateutil.parser.parse('2016-02-21T11:41:43Z')

    # Check that refetching works
    await repo.fetch_data()
