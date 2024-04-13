import os
from pathlib import Path

import pytest

import responses
from netznoe_smartmeter_portal_api import NetzNoeSmartmeterPortalApi


@pytest.fixture
def api():
    return NetzNoeSmartmeterPortalApi(username='localtest', password='localtest')


class ImprovedRequestsMock(responses.RequestsMock):
    def get(self, url, filename, status=200, **kwargs):
        body = self._get_body(filename)
        return self.add(responses.GET, url, body=body, status=status, content_type="application/json", **kwargs)

    def post(self, url, filename, status=200, **kwargs):
        body = self._get_body(filename)
        return self.add(responses.POST, url, body=body, status=status, content_type="application/json", **kwargs)

    @staticmethod
    def _get_body(filename: str):
        return Path(os.path.join(os.path.dirname(__file__), 'responses', f'{filename}.json')).read_text()


@pytest.fixture
def response():
    with ImprovedRequestsMock() as mock:
        yield mock
