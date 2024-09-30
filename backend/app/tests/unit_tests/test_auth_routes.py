import pytest
import inspect
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from app.settings import settings
from app.models import User
from app.routes.auth_routes import (
    register_new_user,
    login_for_access_token,
    get_new_access_token,
    access_token_test
)
from app.routes import auth_routes

from app.routes.auth_routes import UserCreateRequest, TokenHandler
from app.schemas.token_schema import TokenData


@pytest.fixture(autouse=True)
def unwrap_routes(monkeypatch):
    for name, func in inspect.getmembers(auth_routes, inspect.iscoroutinefunction):
        if hasattr(func, '__wrapped__'):
            monkeypatch.setattr(auth_routes, name, func.__wrapped__)


class TestRegisterRoute:

    @pytest.fixture
    def valid_request(self):
        return UserCreateRequest(
            username="testuser",
            password="password123",
            email="test@example.com",
            guest_account=False
        )

    @pytest.fixture
    def mock_register_dependencies(self, monkeypatch, valid_request):
        """Mocks UserCRUD and UserHandler for testing the register route"""
        mock_user_crud = AsyncMock()
        mock_user_handler = AsyncMock()
        monkeypatch.setattr("app.routes.auth_routes.UserCRUD", MagicMock(return_value=mock_user_crud))
        monkeypatch.setattr("app.routes.auth_routes.UserHandler", MagicMock(return_value=mock_user_handler))
        return valid_request, mock_user_crud, mock_user_handler


    async def test_register_new_user_success(self, mock_register_dependencies, mock_session):
        valid_request, mock_user_crud, mock_user_handler = mock_register_dependencies
        mock_user_crud.check_fields_exist.return_value = False
        mock_user_handler.create_user.return_value = {"id": 1, "username": "testuser"}
        result = await register_new_user(valid_request, mock_session)
        assert result['status'] == 'success'
        assert "Account created successfully" in result['message']
        assert 'data' in result
        assert result['data']['id'] == 1
        assert result['data']['username'] == 'testuser'
        mock_user_crud.check_fields_exist.assert_called_once_with(username="testuser", email="test@example.com")
        mock_user_handler.create_user.assert_called_once()


    async def test_register_guest_email_checks(self, mock_register_dependencies, mock_session):
        valid_request, mock_user_crud, mock_user_handler = mock_register_dependencies
        mock_user_crud.check_fields_exist.return_value = False
        valid_request.guest_account = False
        valid_request.email = None
        result = await register_new_user(valid_request, mock_session)
        assert result['status'] == 'success'
        mock_user_handler.create_user.assert_called_once_with(
            username="testuser",
            password="password123",
            email=None,
            guest_account=True
        )


    async def test_register_new_user_username_too_short(self, valid_request, mock_session):
        valid_request.username = "abc"
        with pytest.raises(ValueError, match="Minimum name length is 4"):
            await auth_routes.register_new_user(valid_request, mock_session)


    async def test_register_new_user_password_too_short(self, valid_request, mock_session):
        valid_request.password = "123"
        with pytest.raises(ValueError, match="Please use a longer password"):
            await auth_routes.register_new_user(valid_request, mock_session)


    async def test_register_new_user_already_exists(self, mock_register_dependencies, mock_session):
        valid_request, mock_user_crud, _ = mock_register_dependencies
        mock_user_crud.check_fields_exist.return_value = True
        with pytest.raises(ValueError, match="User with that username or email already exists"):
            await auth_routes.register_new_user(valid_request, mock_session)



class TestLoginRoute:

    @pytest.fixture
    def mock_login_dependencies(self, monkeypatch):
        """Mocks UserService and UserHandler for testing the login route"""
        mock_user_service = AsyncMock()
        mock_user_handler = AsyncMock()
        monkeypatch.setattr("app.routes.auth_routes.UserService", MagicMock(return_value=mock_user_service))
        monkeypatch.setattr("app.routes.auth_routes.UserHandler", MagicMock(return_value=mock_user_handler))
        return mock_user_service, mock_user_handler

    @pytest.fixture
    def mock_run_in_threadpool(self):
        with patch('app.routes.auth_routes.run_in_threadpool') as mock_threadpool:
            yield mock_threadpool

    @pytest.fixture
    def valid_login_form(self):
        return OAuth2PasswordRequestForm(username="testuser", password="password123")


    async def test_login_for_access_token_success(
            self, mock_login_dependencies, mock_run_in_threadpool, valid_login_form, mock_session
    ):
        mock_user_service, mock_user_handler = mock_login_dependencies
        mock_user_service.authenticate_user.return_value = 1
        mock_run_in_threadpool.return_value = "access_token", "refresh_token"
        result = await login_for_access_token(valid_login_form.username, valid_login_form.password, mock_session)
        assert result.status_code == 200
        assert result.body == b'{"message":"Login Successful","access_token":"access_token","refresh_token":"refresh_token"}'
        mock_user_service.authenticate_user.assert_called_once_with("testuser", "password123")
        mock_run_in_threadpool.assert_called_once()


    async def test_login_for_access_token_invalid_credentials(
            self, mock_login_dependencies, mock_run_in_threadpool, valid_login_form, mock_session
    ):
        mock_user_service, _ = mock_login_dependencies
        mock_user_service.authenticate_user.return_value = None
        with pytest.raises(ValueError, match="Incorrect username or password"):
            result = await auth_routes.login_for_access_token(
                valid_login_form.username, valid_login_form.password, mock_session
            )


class TestTokenRoutes:

    @pytest.fixture
    def mock_token_dependencies(self, monkeypatch):
        """Mocks TokenHandler for testing token routes"""
        mock_token_handler = AsyncMock()
        monkeypatch.setattr("app.routes.auth_routes.TokenHandler", mock_token_handler)
        return mock_token_handler

    @pytest.fixture
    def mock_run_in_threadpool(self):
        with patch('app.routes.auth_routes.run_in_threadpool') as mock_threadpool:
            yield mock_threadpool

    @pytest.fixture
    def valid_refresh_token_data(self):
        return {
            'user': {
                'username': 'testuser',
                'user_id': '1'
            },
            'exp': int((datetime.now() + timedelta(minutes=1)).timestamp()),
            'jti': 'some-uuid',
            'refresh': True
        }


    @pytest.fixture
    def mock_refresh_token_bearer(self):
        with patch('app.routes.auth_routes.RefreshTokenBearer') as mock_bearer:
            mock_bearer_instance = mock_bearer.return_value
            mock_bearer_instance.__call__ = AsyncMock()
            yield mock_bearer_instance


    async def test_get_new_access_token_success(
            self, mock_token_dependencies, mock_run_in_threadpool, valid_refresh_token_data, mock_refresh_token_bearer
    ):
        mock_refresh_token_bearer.__call__.return_value = valid_refresh_token_data
        mock_run_in_threadpool.return_value = "new_access_token"
        result = await get_new_access_token(valid_refresh_token_data)
        assert result.status_code == 200
        assert result.body == b'{"access_token":"new_access_token"}'
        mock_run_in_threadpool.assert_called_once_with(
            mock_token_dependencies.create_access_token,
            token_data=TokenData(username='testuser', user_id='1')
        )


    async def test_get_new_access_token_expired(
            self, valid_refresh_token_data, mock_refresh_token_bearer, mock_run_in_threadpool
    ):
        expired_data = valid_refresh_token_data.copy()
        expired_data['exp'] = int((datetime.now() - timedelta(days=1)).timestamp())
        mock_refresh_token_bearer.__call__.return_value = expired_data
        with pytest.raises(HTTPException) as exc_info:
            await get_new_access_token(expired_data)

        assert exc_info.value.status_code == 401
        assert "Invalid or expired login" in str(exc_info.value.detail)

