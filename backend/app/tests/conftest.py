import pytest
from datetime import timedelta

from fastapi.testclient import TestClient

from ..auth.auth_deps import TokenHandler
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


@pytest.fixture
def expired_token(test_user):
    user_data = {"username": test_user.username, "user_id": str(test_user.username)}
    return TokenHandler.create_access_token(
        user_data=user_data,
        expires_delta=timedelta(microseconds=1)
    )

