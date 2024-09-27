import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from unittest.mock import AsyncMock, MagicMock, patch
from app.routes.auth_routes import register_new_user
from app.routes.auth_routes import UserCreateRequest
from app.models import User


@pytest.fixture
def mock_dependencies(monkeypatch):
    mock_user_crud = AsyncMock()
    mock_user_handler = AsyncMock()
    monkeypatch.setattr("app.routes.auth_routes.BaseCRUD", MagicMock(return_value=mock_user_crud))
    monkeypatch.setattr("app.routes.auth_routes.UserHandler", MagicMock(return_value=mock_user_handler))
    return mock_user_crud, mock_user_handler


@pytest.fixture
def valid_request():
    return UserCreateRequest(
        username="testuser",
        password="password123",
        email="test@example.com",
        guest_account=False
    )

async def test_register_new_user_success(mock_dependencies, valid_request, mock_session):
    mock_user_crud, mock_user_handler = mock_dependencies
    mock_user_crud.check_fields_exist.return_value = False
    mock_user_handler.create_user.return_value = {"id": 1, "username": "testuser"}
    result = await register_new_user(valid_request, mock_session)
    assert "Account created successfully" in result['message']
    assert 'data' in result
    assert result['data']['id'] == 1
    assert result['data']['username'] == 'testuser'
    mock_user_crud.check_fields_exist.assert_called_once_with(username="testuser", email="test@example.com")
    mock_user_handler.create_user.assert_called_once()


async def test_register_new_user_username_too_short(mock_dependencies, mock_session):
    request = UserCreateRequest(username="abc", password="password123", email="test@example.com")
    with pytest.raises(HTTPException, match="Minimum name length is 4"):
        await register_new_user(request, mock_session)


@pytest.mark.asyncio
async def test_register_new_user_password_too_short(mock_dependencies, mock_session):
    request = UserCreateRequest(username="testuser", password="12345", email="test@example.com")
    with pytest.raises(HTTPException, match="Please use a longer password"):
        await register_new_user(request, mock_session)


@pytest.mark.asyncio
async def test_register_new_user_already_exists(mock_dependencies, valid_request, mock_session):
    mock_user_crud, _ = mock_dependencies
    mock_user_crud.check_fields_exist.return_value = True
    with pytest.raises(HTTPException, match="User with that username or email already exists"):
        await register_new_user(valid_request, mock_session)


@pytest.mark.asyncio
async def test_register_new_user_guest_account_with_email(mock_dependencies, mock_session):
    request = UserCreateRequest(
        username="testuser", password="password123", email="test@example.com", guest_account=True
    )
    with pytest.raises(HTTPException, match="You're not supposed to be doing that"):
        await register_new_user(request, mock_session)


@pytest.mark.asyncio
async def test_register_new_user_non_guest_without_email(mock_dependencies, mock_session):
    with pytest.raises(ValidationError):
        request = UserCreateRequest(username="testuser", password="password123", guest_account=False)
        await register_new_user(request, mock_session)
