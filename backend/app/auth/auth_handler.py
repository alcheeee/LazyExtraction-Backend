from fastapi import Depends

from jose import JWTError, exceptions
from sqlalchemy import select

from .auth_deps import PasswordSecurity, TokenHandler
from ..crud.user_crud import UserCRUD
from ..models import User
from ..database import redis_client, get_db
from ..utils import CommonHTTPErrors
from ..config import settings
from ..database.db import get_session


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

    @staticmethod
    async def check_if_admin(auth_token: str = Depends(settings.oauth2_scheme)):
        try:
            payload = TokenHandler.decode_token(auth_token)
            user_data = payload.get("user")
            if not user_data:
                raise CommonHTTPErrors.credentials_error(data=payload)

            user_id = int(user_data['user_id'])
            async with get_session() as session:
                user_crud = UserCRUD(User, session)
                admin_name = await user_crud.is_user_admin(user_id)
                if not admin_name:
                    raise CommonHTTPErrors.credentials_error(data=user_data)
                return admin_name
        except Exception as e:
            raise e

