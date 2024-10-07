import pytest
import asyncio


@pytest.mark.anyio
async def test_user_registration(async_client, test_user):
    data = {
        'username': test_user['username'],
        'password': test_user['password'],
        'email': test_user['email']
    }
    response = await async_client.post("/user/register", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'success'
    assert response_data['user-data']['access_token']
    assert response_data['user-data']['refresh_token']
    assert response_data['user-data']['inventory']
    assert response_data['user-data']['stats']
    assert response_data['user-data']['trainingprogress']


@pytest.mark.anyio
async def test_registration_missing_fields(async_client):
    register_input = {'username': None, 'password': 'test_password', 'email': None}
    response = await async_client.post("/user/register", json=register_input)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_registration_existing_username(async_client, register_test_user):
    register_input = {
        'username': register_test_user['user-data']['user']['username'],  # Existing username
        'password': 'test_password',
        'email': 'new_email@test.com'
    }
    response = await async_client.post("/user/register", json=register_input)
    assert response.status_code == 400


@pytest.mark.anyio
async def test_registration_existing_email(async_client, register_test_user):
    register_input = {
        'username': 'new_user',
        'password': 'test_password',
        'email': register_test_user['user-data']['user']['email']  # Existing email
    }
    response = await async_client.post("/user/register", json=register_input)
    assert response.status_code == 400


@pytest.mark.anyio
async def test_registration_invalid_email_format(async_client):
    register_input = {
        'username': 'new_user_invalid_email',
        'password': 'test_password',
        'email': 'invalid-email-format'  # Invalid email format
    }
    response = await async_client.post("/user/register", json=register_input)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_registration_invalid_username_length(async_client):
    register_input = {
        'username': '123',  # Too short
        'password': 'test_length',
        'email': 'test-blank@test.com'
    }
    response = await async_client.post("/user/register", json=register_input)
    assert response.status_code == 400


@pytest.mark.anyio
async def test_user_login(async_client, register_test_user):
    data = {
        'username': register_test_user['user-data']['user']['username'],
        'password': register_test_user['user-data']['user']['password']
    }
    response = await async_client.post("/user/login", data=data)
    assert response.status_code == 200
    response_data = response.json()
    assert 'access_token' in response_data


@pytest.mark.anyio
async def test_registration_missing_fields(async_client):
    register_input = {'username': None, 'password': 'test_password', 'email': None}
    response = await async_client.post("/user/register", json=register_input)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_token_expiration(async_client, expired_token):
    import time
    await asyncio.sleep(1)
    response = await async_client.post(
        "user/test/test-token",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_valid_refresh_token(async_client, register_test_user):
    refresh_response = await async_client.post(
        "/user/refresh-token",
        headers={"Authorization": f"Bearer {register_test_user['user-data']['refresh_token']}"}
    )
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()


@pytest.mark.anyio
async def test_refresh_token_as_access(async_client, register_test_user):
    access_response = await async_client.post(
        "user/test/test-token",
        headers={"Authorization": f"Bearer {register_test_user['user-data']['refresh_token']}"}
    )
    assert access_response.status_code == 401


@pytest.mark.anyio
async def test_access_token_as_refresh(async_client, register_test_user):
    refresh_response = await async_client.post(
        "user/refresh-token",
        headers={"Authorization": f"Bearer {register_test_user['user-data']['access_token']}"}
    )
    assert refresh_response.status_code == 401
