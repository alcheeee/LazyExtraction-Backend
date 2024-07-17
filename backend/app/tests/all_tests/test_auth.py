import pytest
from . import Check, user, second_user


class TestRegister:
    """
    Tests a valid registration request, and various invalid registration requests
    """

    def test_register(self, client):
        data = {
            'username': user.username,
            'password': user.password,
            'email': user.email
        }
        response = client.post("/user/register", json=data)
        Check.valid_request(response)

        # Creating a second user for follow-up tests
        if response.status_code == 200:
            data['username'] = second_user.username
            data['email'] = second_user.email
            response = client.post("/user/register", json=data)
            Check.valid_request(response)

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
