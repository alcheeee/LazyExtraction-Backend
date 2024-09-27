from fastapi import Depends
from fastapi.concurrency import run_in_threadpool
from jose import JWTError, exceptions
from sqlalchemy import select
from .auth_deps import PasswordSecurity, TokenHandler
from app.crud.user_crud import UserCRUD
from app.models import User
from app.utils import CommonHTTPErrors
from app.settings import settings


class UserService:
    def __init__(self, session):
        self.session = session
        self.user_crud = UserCRUD(User, session)
        self.password_security = PasswordSecurity

    async def get_user_pass_id_by_username(self, username: str):
        try:
            result = await self.session.execute(
                select(User.password, User.id)
                .where(User.username == username)  # type: ignore
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
        check_hash = await run_in_threadpool(self.password_security.check_pass_hash, password, user_password)
        if user_password and check_hash:
            return user_id
        return False

