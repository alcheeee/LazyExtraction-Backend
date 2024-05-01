from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy import select
from .auth_bearer import oauth2_scheme
from .auth_deps import password_security, token_handler
from ..crud.BaseCRUD import EnhancedCRUD
from ..models.models import User
from ..database.db import get_session
from ..utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()


class UserService:
    def __init__(self, session):
        self.session = session
        self.user_crud = EnhancedCRUD(User, session)

    async def get_user_pass_id_by_username(self, username: str):
        try:
            result = await self.session.execute(
                select(User.password, User.id).where(User.username == username)
            )
            user_data = result.first()
            if user_data:
                return user_data
            return None
        except Exception as e:
            return None

    async def authenticate_user(self, username: str, password: str):
        user_pass_id = await self.get_user_pass_id_by_username(username)
        if not user_pass_id:
            return False
        user_password, user_id = user_pass_id
        if user_password and await password_security.check_pass_hash(password, user_password):
            return user_id
        return False


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = token_handler.decode_token(token=token)
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    async with get_session() as session:
        try:
            user_crud = EnhancedCRUD(User, session)
            user = await user_crud.get_by_id(int(user_id))
            if not user:
                raise credentials_exception
            return user
        except NoResultFound:
            raise credentials_exception
