import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.database.user_handler import UserHandler
from app.auth.auth_deps import PasswordSecurity, TokenData
from app.schemas.token_schema import TokenData
from app.models.models import User


@pytest.fixture
def mock_hash_password():
    with patch('app.auth.auth_deps.PasswordSecurity.hash_password') as mock:
        return mock.return_value


@pytest.fixture
def handler(mock_session, mock_hash_password):
    handler = UserHandler(mock_session)
    handler.create_tokens = Mock(return_value=("access_token_mock", "refresh_token_mock"))
    handler.mock_hash_password = "hashed_password_mock"
    mock_session.add_all = Mock()
    return handler


class TestUserHandle:

    async def test_create_user_success(self, handler, mock_session):
        result = await handler.create_user("testuser", "testpassword", "testuser@example.com")
        assert result['access_token'] == "access_token_mock"
        assert result['refresh_token'] == "refresh_token_mock"
        assert result['username'] == "testuser"
        assert result['guest_account'] is False
        assert 'inventory' in result
        assert 'stats' in result
        assert 'trainingprogress' in result
        mock_session.commit.assert_awaited_once()


    async def test_create_guest_user(self, handler, mock_session):
        result = await handler.create_user("guestuser", "testpassword", None, guest_account=True)
        mock_session.commit.assert_awaited_once()
        assert result['username'] == "guestuser"
        assert result['guest_account'] is True


    async def test_create_game_bot(self, handler, mock_session):
        result = await handler.create_user("botuser", "testpassword", "bot@example.com", game_bot=True)
        mock_session.commit.assert_awaited_once()
        assert isinstance(result, User)
        assert result.username == "botuser"
