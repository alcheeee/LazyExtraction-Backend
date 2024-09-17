import pytest
from . import user, second_user, Check


class TestRegister:

    def test_register(self, client, test_user):
        data = {
            'username': test_user.username,
            'password': test_user.password,
            'email': test_user.email
        }
        response = client.post("/user/register", json=data)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['status'] == 'success'

        # Creating a second user for follow-up tests
        if response.status_code == 200:
            data['username'] = second_user.username
            data['email'] = second_user.email
            response = client.post("/user/register", json=data)
            response_data = response.json()
            assert response_data['status'] == 'success'

    @pytest.mark.parametrize(
        "register_input, expected_status_code",
        [
            # Missing fields
            ({'username': None, 'password': 'test_password', 'email': None}, 422),
            # Existing username
            ({'username': user.username, 'password': 'test_password', 'email': 'new_email@test.com'}, 400),
            # Existing email
            ({'username': 'new_user', 'password': 'test_password', 'email': user.email}, 400),
            # Invalid email format
            ({'username': 'new_user_invalid_email', 'password': 'test_password', 'email': 'invalid-email-format'}, 422),
            # Invalid username length
            ({'username': '123', 'password': 'test_length', 'email': 'test-blank@test.com'}, 400)
        ]
    )
    def test_invalid_registrations(self, client, register_input, expected_status_code):
        response = client.post("/user/register", json=register_input)
        assert response.status_code == expected_status_code
        if response.status_code == 200:
            data = response.json()
            assert data['status'] == 'success'


class TestLogin:

    def test_login(self, client, test_user):
        data = {
            'username': test_user.username,
            'password': test_user.password
        }
        response = client.post("/user/login", data=data)
        Check.valid_login(response, test_user)

        # Get auth_token for second user
        if response.status_code == 200:
            data['username'] = second_user.username
            data['password'] = second_user.password
            response = client.post("/user/login", data=data)
            Check.valid_login(response, second_user)

    @pytest.mark.parametrize(
        "login_input, expected_status_code",
        [
            # Missing fields
            ({'username': None, 'password': 'test_password'}, 422),
            ({'username': 'test_user', 'password': None}, 422),
            ({'username': None, 'password': None}, 422),
            # Wrong password
            ({'username': 'existing_user', 'password': 'wrong_password'}, 400),
            # Invalid account
            ({'username': 'non_existent_user', 'password': 'any_password'}, 400)
        ]
    )
    def test_invalid_logins(self, client, login_input, expected_status_code):
        response = client.post("/user/login", data=login_input)
        assert response.status_code == expected_status_code


class TestAuthTokens:
    def test_token_expiration(self, client, expired_token):
        import time
        time.sleep(1)
        response = client.post(
            "user/test/test-token",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401

    def test_valid_refresh_token(self, client, test_user):
        refresh_response = client.post(
            "/user/refresh-token",
            headers={"Authorization": f"Bearer {test_user.refresh_token}"}
        )
        assert refresh_response.status_code == 200
        assert "access_token" in refresh_response.json()

    def test_refresh_token_as_access(self, client, test_user):
        access_response = client.post(
            "user/test/test-token",
            headers={"Authorization": f"Bearer {test_user.refresh_token}"}
        )
        assert access_response.status_code == 401

    def test_access_token_as_refresh(self, client, test_user):
        refresh_response = client.post(
            "user/refresh-token",
            headers={"Authorization": f"Bearer {test_user.auth_token}"}
        )
        assert refresh_response.status_code == 401