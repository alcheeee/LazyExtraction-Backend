from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.requests import Request
from fastapi.concurrency import run_in_threadpool

from .auth_deps import TokenHandler
from app.settings import settings
from app.utils import CommonHTTPErrors


class TokenBearer(HTTPBearer):
    """
    Returns Dictionary = {
        {'user': {
            'username': str(username),
            'user_id': str(user_id)
        },
        'exp': int(expiration),
        'jti': str(uuid4),
        'refresh': False
    }
    """
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = await run_in_threadpool(TokenHandler.decode_token, token)
        if not self.token_valid:
            raise CommonHTTPErrors.credentials_error()

        await self.verify_token_data(token_data)

        return token_data

    @staticmethod
    async def token_valid(token: str) -> bool:
        token_data = await run_in_threadpool(TokenHandler.decode_token, token)
        return True if token_data is not None else False

    async def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please Override this method")


class AccessTokenBearer(TokenBearer):
    async def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise CommonHTTPErrors.credentials_error(message="Provide an access token", data=token_data)


class RefreshTokenBearer(TokenBearer):
    async def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise CommonHTTPErrors.credentials_error(message="Provide a refresh token", data=token_data)
