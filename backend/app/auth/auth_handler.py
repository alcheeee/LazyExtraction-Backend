from fastapi import Depends
from jose import JWTError
from sqlalchemy import select

from .auth_bearer import oauth2_scheme
from .auth_deps import PasswordSecurity, token_handler
from ..crud.user_crud import UserCRUD
from ..models import User
from ..database import get_session, redis_client
from ..utils import common_http_errors, RetryDecorators


class UserService:
    def __init__(self, session):
        self.session = session
        self.user_crud = UserCRUD(User, session)

    async def get_user_pass_id_by_username(self, username: str):
        try:
            result = await self.session.execute(
                select(User.password, User.id)
                .where(User.username == username)
            )
            user_data = result.first()
            if user_data:
                return user_data
            return None
        except Exception:
            return None

    @RetryDecorators.function_retry_decorator()
    async def authenticate_user(self, username: str, password: str):
        user_pass_id = await self.get_user_pass_id_by_username(username)
        if not user_pass_id:
            return False
        user_password, user_id = user_pass_id
        if user_password and await PasswordSecurity.check_pass_hash(password, user_password):
            return user_id
        return False


class CurrentUser:
    def __init__(self):
        self.user_cache_ttl = 300
        self.token_cache_ttl = 60

    @staticmethod
    async def _decode_token(token: str) -> dict:
        return await token_handler.decode_token(token)

    async def verify_payload(self, token: str) -> int:
        cached_user_id = await redis_client.get_cache(f"token:{token}")
        if cached_user_id:
            return int(cached_user_id)
        try:
            payload = await self._decode_token(token)
            user_id = payload.get("sub")
            if not user_id:
                raise common_http_errors.credentials_error()

            user_id = int(user_id)
            await redis_client.set_cache(f"token:{token}", str(user_id), expire=self.token_cache_ttl)
            return user_id

        except (JWTError, ValueError):
            raise common_http_errors.credentials_error()

    async def ensure_user_exists(self, token: str = Depends(oauth2_scheme)):
        user_id = await self.verify_payload(token)
        user_exists = await redis_client.get_cache(f"user_exists:{user_id}")
        if user_exists:
            return user_id

        async with get_session() as session:
            user_crud = UserCRUD(User, session)
            exists = await user_crud.get_user_field_from_id(user_id, 'id')
            if not exists:
                raise common_http_errors.credentials_error()

            await redis_client.set_cache(f"user_exists:{user_id}", "1", expire=self.user_cache_ttl)
            return user_id

    async def check_if_admin(self, token: str = Depends(oauth2_scheme)):
        user_id = await self.verify_payload(token)
        async with get_session() as session:
            user_crud = UserCRUD(User, session)
            admin_name = await user_crud.is_user_admin(user_id)
            if not admin_name:
                raise common_http_errors.credentials_error()
            return admin_name


current_user = CurrentUser()
