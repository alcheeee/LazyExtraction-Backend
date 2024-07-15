import pytest
from .response import Check
from .conftest import UserAccount


class TestRoutes:
    """
    Make sure all routes are responding
    """

    @pytest.mark.parametrize(
        "route, expected_status_code",
        [
            # Routes
            ('user', 200),
            ('crews', 200),
            ('game', 200),
            ('market', 200),
            ('info', 200)
        ]
    )
    def test_routes(self, client, route, expected_status_code):
        response = client.get(f"/{route}")
        assert response.status_code == expected_status_code
        Check.valid_request(response)


    @pytest.mark.xfail
    def test_admin_route(self, client, test_user):
        headers = {"Authorization": f"Bearer {test_user.auth_token}"}
        response = client.get('/admin', headers=headers)
        assert response.status_code == 401
        Check.valid_request(response)


class TestRegister:
    """
    Tests a valid registration request, and various invalid registration requests
    """
    register_test = UserAccount()

    def test_register(self, client):
        data = {
            'username': self.register_test.username,
            'password': self.register_test.password,
            'email': self.register_test.email
        }
        response = client.post("/user/register", json=data)
        Check.valid_request(response)

    @pytest.mark.parametrize(
        "register_input, expected_status_code",
        [
            # Missing fields
            ({'username': None, 'password': 'test_password', 'email': None}, 422),
            # Same username
            ({'username': register_test.username, 'password': 'test_password', 'email': 'new_email@LETests.com'}, 400),
            # Same email
            ({'username': 'new_user', 'password': 'test_password', 'email': f'{register_test.email}@LETests.com'}, 400),
            # Invalid email format
            ({'username': 'new_user_invalid_email', 'password': 'test_password', 'email': 'invalid-email-format'}, 422)
        ]
    )
    @pytest.mark.xfail
    def test_invalid_registrations(self, client, register_input, expected_status_code):
        response = client.post("/user/register", json=register_input)
        assert response.status_code == expected_status_code
        Check.valid_request(response)


class TestLogin:
    """
    Tests a valid login request, obtaining a valid Authorization Token, and various invalid login requests
    """
    def test_login(self, client, test_user):
        data = {
            'username': test_user.username,
            'password': test_user.password
        }
        response = client.post("/user/login", data=data)
        assert response.status_code == 200
        data = response.json()
        assert 'access_token' in data
        assert data['access_token'] is not None
        token = data['access_token']
        test_user.auth_token = token

    @pytest.mark.parametrize(
        "login_input, expected_status_code",
        [
            # Missing fields
            ({'username': None, 'password': 'test_password'}, 422),
            ({'username': 'test_user', 'password': None}, 422),
            ({'username': None, 'password': None}, 422),
            # Wrong password
            ({'username': 'existing_user', 'password': 'wrong_password'}, 401),
            # Invalid account
            ({'username': 'non_existent_user', 'password': 'any_password'}, 401)
        ]
    )
    @pytest.mark.xfail
    def test_invalid_logins(self, client, login_input, expected_status_code):
        response = client.post("/user/login", json=login_input)
        assert response.status_code == expected_status_code
        Check.valid_request(response)
