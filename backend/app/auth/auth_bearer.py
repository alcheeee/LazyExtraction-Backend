from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.requests import Request

from .auth_deps import TokenHandler
from ..config import settings
from ..utils import CommonHTTPErrors


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
        token_data = TokenHandler.decode_token(token)
        if not self.token_valid:
            raise CommonHTTPErrors.credentials_error()

        self.verify_token_data(token_data)

        return token_data

    @staticmethod
    def token_valid(token: str) -> bool:
        token_data = TokenHandler.decode_token(token)
        return True if token_data is not None else False

    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please Override this method")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise CommonHTTPErrors.credentials_error(message="Provide an access token", data=token_data)


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise CommonHTTPErrors.credentials_error(message="Provide a refresh token", data=token_data)
