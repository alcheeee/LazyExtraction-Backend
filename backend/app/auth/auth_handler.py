from fastapi import Depends

from jose import JWTError
from sqlalchemy import select

from .auth_deps import PasswordSecurity, TokenHandler
from ..crud.user_crud import UserCRUD
from ..models import User
from ..database import get_session, redis_client
from ..utils import CommonHTTPErrors
from ..config import settings


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

    @staticmethod
    async def verify_payload(token: str) -> int:
        try:
            payload = await TokenHandler.decode_token(token)
            user_data = payload.get("user")
            if not user_data:
                raise CommonHTTPErrors.credentials_error()

            return user_data

        except (JWTError, ValueError):
            raise CommonHTTPErrors.credentials_error()

    async def check_if_admin(self, auth_token: str = Depends(settings.oauth2_scheme)):
        user_data = await self.verify_payload(auth_token)
        user_id = int(user_data['user']['user_id'])
        async with get_session() as session:
            user_crud = UserCRUD(User, session)
            admin_name = await user_crud.is_user_admin(user_id)
            if not admin_name:
                raise CommonHTTPErrors.credentials_error()
            return admin_name


current_user = CurrentUser()
