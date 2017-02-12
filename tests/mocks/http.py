import json
import urllib.parse
import os

import pytest

FAKE_RESPONSES = {
    '/users/reupen': 'users/reupen.json',
    '/users/reupen/repos': 'users/reupen/repos.json',
    '/repos/reupen/columns_ui': 'repos/reupen/columns_ui.json',
    '/repos/reupen/columns_ui/branches':
        'repos/reupen/columns_ui/branches.json'
}


class MockResponse:
    def __init__(self, content, status_code=200, headers=None):
        self._content = content
        self.headers = headers if headers is not None else {}
        self.status = status_code

    async def json(self):
        return self._content

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aenter__(self):
        return self


def get_mock(session, url, headers=None, params=None):
    headers = headers if headers is not None else {}
    params = params if params is not None else {}

    url_parts = urllib.parse.urlsplit(url)
    assert url_parts.path in FAKE_RESPONSES

    path = os.path.join(os.path.dirname(__file__), '..', 'mock_data',
                        FAKE_RESPONSES[url_parts.path])

    with open(path) as f:
        data = json.load(f)

    return MockResponse(data)


@pytest.fixture(autouse=True)
def fake_response(monkeypatch):
    monkeypatch.setattr("aiohttp.ClientSession.get", get_mock)
