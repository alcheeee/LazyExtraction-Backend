import pytest
from fastapi.testclient import TestClient
from .testing_utils import UserAccount, Check
from ..main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app=app, base_url='http://127.0.0.1:8000/') as client:
        yield client


@pytest.fixture(scope="module")
def test_user():
    account = UserAccount()
    return account


def test_user_route(client):
    response = client.get("/user")
    Check.valid_request(response)


def test_register(client, test_user):
    data = {
        'username': test_user.username,
        'password': test_user.password,
        'email': test_user.email
    }
    response = client.post("/user/register", json=data)
    Check.valid_request(response)


def test_login(client, test_user):
    data = {
        'username': test_user.username,
        'password': test_user.password
    }
    response = client.post("/user/login", data=data)
    token = Check.valid_login_request(response)
    test_user.auth_token = token


@pytest.mark.xfail
def test_login_wrong_password(client, test_user):
    data = {
        'username': test_user.username,
        'password': f"{test_user.password}1"
    }
    response = client.post("/user/login", data=data)
    Check.valid_login_request(response)


@pytest.mark.xfail
def test_login_invalid_account(client, test_user):
    data = {
        'username': "user",
        'password': "userpassword"
    }
    response = client.post("/user/login", data=data)
    Check.valid_login_request(response)


@pytest.mark.xfail
def test_register_missing_fields(client, test_user):
    data = {
        'username': None,
        'password': test_user.password,
        'email': None
    }
    response = client.post("user/register", json=data)
    Check.valid_request(response)


@pytest.mark.xfail
def test_register_same_username(client, test_user):
    data = {
        'username': test_user.username,
        'password': test_user.password,
        'email': f"{test_user.username}invalid@LETests.com"
    }
    response = client.post("user/register", json=data)
    Check.valid_request(response)


@pytest.mark.xfail
def test_register_same_email(client, test_user):
    data = {
        'username': f"{test_user.username}invalid",
        'password': test_user.password,
        'email': test_user.email
    }
    response = client.post("user/register", json=data)
    Check.valid_request(response)


@pytest.mark.xfail
def test_register_invalid_email(client, test_user):
    data = {
        'username': f"{test_user.username}invalid",
        'password': test_user.password,
        'email': "invalid-format@"
    }
    response = client.post("user/register", json=data)
    Check.valid_request(response)




