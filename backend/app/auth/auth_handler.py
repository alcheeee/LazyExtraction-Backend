from fastapi import Depends
from jose import JWTError
from sqlalchemy import select, exc
from .auth_bearer import oauth2_scheme
from .auth_deps import password_security, token_handler
from ..crud.user_crud import UserCRUD
from ..models import User
from ..database import get_session
from ..utils import common_http_errors


class UserService:
    def __init__(self, session):
        self.session = session
        self.user_crud = UserCRUD(User, session)

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


class CurrentUser:

    def verify_payload(self, token):
        try:
            payload = token_handler.decode_token(token=token)
            user_id = payload.get("sub")
            if not user_id:
                print("No User ID")
                raise common_http_errors.credentials_error()
            return int(user_id)
        except JWTError as JWTe:
            print(str(JWTe))
            raise common_http_errors.credentials_error()

    async def ensure_user_exists(self, token: str = Depends(oauth2_scheme)):
        user_id = self.verify_payload(token=token)
        async with get_session() as session:
            user_crud = UserCRUD(User, session)
            exists = await user_crud.get_user_field_from_id(user_id, 'id')
            if not exists:
                raise common_http_errors.credentials_error()
            return user_id

    async def get_all_user_info(self, token: str = Depends(oauth2_scheme)):
        user_id = self.verify_payload(token=token)
        async with get_session() as session:
            user_crud = UserCRUD(User, session)
            user = await user_crud.get_by_id(user_id)
            if not user:
                raise common_http_errors.credentials_error()
            return user

    async def check_if_admin(self, token: str = Depends(oauth2_scheme)):
        user_id = self.verify_payload(token=token)
        async with get_session() as session:
            user_crud = UserCRUD(User, session)
            admin_name = await user_crud.is_user_admin(user_id)
            if not admin_name:
                raise common_http_errors.credentials_error()
            return admin_name


current_user = CurrentUser()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = token_handler.decode_token(token=token)
        user_id = payload.get("sub")
        if not user_id:
            raise common_http_errors.credentials_error()
    except JWTError:
        raise common_http_errors.credentials_error()

    async with get_session() as session:
        try:
            user_crud = UserCRUD(User, session)
            user_exists = await user_crud.exists_by_id(int(user_id))
            if not user_exists:
                raise common_http_errors.credentials_error()
            return user_exists
        except exc.NoResultFound:
            raise common_http_errors.credentials_error()
