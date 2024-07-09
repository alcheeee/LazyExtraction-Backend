import pytest
from httpx import AsyncClient
from ..main import app
from ..database.db import get_db
from unittest.mock import AsyncMock
import datetime


@pytest.mark.anyio
async def test_register_success():
    account = f"dev-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    mock_db_session = AsyncMock()
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post('/user/register',
                                     json={
                                         "username": account,
                                         "password": account,
                                         "email": f"{account}@example.com"
                                     })

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": f"Account created, welcome {account}"}


@pytest.mark.anyio
async def test_register_existing_user():
    account = f"dev-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    mock_db_session = AsyncMock()
    mock_db_session.execute.return_value.scalar_one_or_none.side_effect = [None, True]

    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post('/user/register',
                          json={
                              "username": account,
                              "password": account,
                              "email": f"{account}@example.com"
                          })
        response = await client.post('/user/register',
                                     json={
                                         "username": account,
                                         "password": account,
                                         "email": f"{account}@example.com"
                                     })

    app.dependency_overrides.clear()
    assert response.status_code == 400
    assert "User with that username or email already exists" in response.json()["detail"]


@pytest.mark.anyio
async def test_register_invalid_email():
    account = f"dev-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    mock_db_session = AsyncMock()

    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post('/user/register',
                                     json={
                                         "username": account,
                                         "password": account,
                                         "email": "invalid_email"
                                     })
    app.dependency_overrides.clear()
    assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.anyio
async def test_login_success():
    account = f"dev-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    mock_db_session = AsyncMock()
    mock_db_session.execute.return_value.scalar_one_or_none.side_effect = [None, {"id": 1, "username": account}]

    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post('/user/register',
                          json={
                              "username": account,
                              "password": account,
                              "email": f"{account}@example.com"
                          })
        response = await client.post('/user/login',
                                     data={
                                         "username": account,
                                         "password": account,
                                     })

    app.dependency_overrides.clear()
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_invalid_credentials():
    account = f"dev-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    mock_db_session = AsyncMock()
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post('/user/login',
                                     data={
                                         "username": account,
                                         "password": "wrong_password",
                                     })

    app.dependency_overrides.clear()
    assert response.status_code == 400
    assert "Incorrect username or password" in response.json()["detail"]