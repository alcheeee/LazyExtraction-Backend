from typing import Optional
import pytest
from fastapi.testclient import TestClient
from ..main import app


class UserAccount:
    def __init__(self, username="test-user"):
        self.username: str = f"{username}"
        self.email: str = f"{self.username}@LETests.com"
        self.password: str = f"123456"
        self.auth_token: Optional[str] = None


@pytest.fixture(scope="module")
def client():
    with TestClient(app=app, base_url='http://127.0.0.1:8000/') as client:
        yield client


@pytest.fixture(scope="module")
def test_user(client):
    user = UserAccount()
    return user
