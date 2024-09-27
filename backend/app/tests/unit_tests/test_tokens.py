import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool

from factory import Factory
from unittest.mock import patch, Mock, AsyncMock
from jose import jwt

from app.auth.auth_deps import TokenHandler
from app.database.user_handler import UserHandler
from app.auth.auth_bearer import AccessTokenBearer, RefreshTokenBearer
from app.schemas.token_schema import TokenData
from app.settings import settings


class TokenDataFactory(Factory):
    class Meta:
        model = TokenData

    username = 'testuser'
    user_id = '123456'


@pytest.fixture
def token_data():
    return TokenDataFactory()


class TestTokens:

    async def test_create_access_token(self, token_data):
        token = TokenHandler.create_access_token(token_data)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded['user']['username'] == token_data.username
        assert decoded['user']['user_id'] == token_data.user_id
        assert not decoded['refresh']


    async def test_create_refresh_token(self, token_data):
        token = TokenHandler.create_access_token(token_data, refresh=True)
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded['user']['username'] == token_data.username
        assert decoded['user']['user_id'] == token_data.user_id
        assert decoded['refresh']


    async def test_decode_token(self, token_data):
        token = TokenHandler.create_access_token(token_data)
        decoded = await run_in_threadpool(TokenHandler.decode_token, token)
        assert decoded['user']['username'] == token_data.username
        assert decoded['user']['user_id'] == token_data.user_id


    @patch('app.auth.auth_deps.datetime')
    async def test_async_decode_expired_token(self, mock_datetime, token_data):
        from fastapi.concurrency import run_in_threadpool
        mock_datetime.now.return_value = datetime.now() - timedelta(days=1)
        token = TokenHandler.create_access_token(token_data)
        with pytest.raises(HTTPException) as exc_info:
            await run_in_threadpool(TokenHandler.decode_token, token)
        assert exc_info.value.status_code == 401


    async def test_valid_access_token(self, token_data):
        token = TokenHandler.create_access_token(token_data)
        bearer = AccessTokenBearer()
        request = Mock()
        request.headers = {"Authorization": f"Bearer {token}"}
        result = await bearer(request)
        assert result['user']['username'] == token_data.username
        assert result['user']['user_id'] == token_data.user_id


    async def test_invalid_refresh_token(self, token_data):
        token = TokenHandler.create_access_token(token_data, refresh=True)
        bearer = AccessTokenBearer()
        request = Mock()
        request.headers = {"Authorization": f"Bearer {token}"}
        with pytest.raises(HTTPException) as exc_info:
            await bearer(request)
        assert exc_info.value.status_code == 401


    async def test_valid_refresh_token(self, token_data):
        token = TokenHandler.create_access_token(token_data, refresh=True)
        bearer = RefreshTokenBearer()
        request = Mock()
        request.headers = {"Authorization": f"Bearer {token}"}
        result = await bearer(request)
        assert result['user']['username'] == token_data.username
        assert result['user']['user_id'] == token_data.user_id


    async def test_invalid_access_token(self, token_data):
        token = TokenHandler.create_access_token(token_data)
        bearer = RefreshTokenBearer()
        request = Mock()
        request.headers = {"Authorization": f"Bearer {token}"}
        with pytest.raises(HTTPException) as exc_info:
            await bearer(request)
        assert exc_info.value.status_code == 401


    @patch('app.auth.auth_handler.TokenHandler.create_access_token')
    async def test_create_tokens(self, mock_create_access_token, token_data):
        mock_create_access_token.side_effect = ["access_token_mock", "refresh_token_mock"]
        access_token, refresh_token = UserHandler.create_tokens(token_data)
        assert access_token == "access_token_mock"
        assert refresh_token == "refresh_token_mock"
        mock_create_access_token.assert_any_call(
            token_data=token_data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        mock_create_access_token.assert_any_call(
            token_data=token_data, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), refresh=True
        )


