import pytest
from fastapi.testclient import TestClient

from .account_util import UserAccount
from ..main import app


user = UserAccount()
second_user = UserAccount("test-user-2")


@pytest.fixture(scope="module")
def client():
    with TestClient(app=app, base_url='http://127.0.0.1:8000/') as client:
        yield client


@pytest.fixture(scope="module")
def test_user(client):
    return user
