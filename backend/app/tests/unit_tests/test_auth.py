import pytest
from unittest.mock import patch, AsyncMock, Mock
from app.auth.auth_handler import UserService


@pytest.fixture
def handler(mock_session):
    handler = UserService(mock_session)
    handler.get_user_pass_id_by_username = AsyncMock(return_value=("hashed_password", "user_id"))
    handler.password_security = Mock()
    handler.password_security.check_pass_hash = Mock()
    return handler


class TestAuthenticateUser:

    async def test_authenticate_user_success(self, handler):
        handler.password_security.check_pass_hash.return_value = True
        handler.mock_hash = True
        result = await handler.authenticate_user("testuser", "password")
        assert result == "user_id"


    async def test_authenticate_user_wrong_password(self, handler):
        handler.password_security.check_pass_hash.return_value = False
        result = await handler.authenticate_user("testuser", "wrongpassword")
        assert result is False


    async def test_authenticate_user_user_not_found(self, handler):
        handler.get_user_pass_id_by_username.return_value = None
        result = await handler.authenticate_user("testuser", "password")
        assert result is False
