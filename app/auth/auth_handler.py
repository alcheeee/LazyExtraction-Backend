from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from .auth_bearer import SECRET_KEY, ALGORITHM, oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES
from ..database.UserHandler import user_crud
from ..utils.logger import MyLogger
import bcrypt
user_log = MyLogger.user()
admin_log = MyLogger.admin()


class UserAuthenticator:
    def __init__(self, user_data_manager):
        self.user_data_manager = user_data_manager


    async def authenticate_user(self, username: str, password: str):
        user = await self.user_data_manager.get_user_by_username(username)
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            admin_log.warning(f"Authentication failed for User {username}.")
            return False
        admin_log.info(f"User {username} logged in successfully.")
        return user


    def create_access_token(self, user_id: int, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        data = {"sub": str(user_id)}
        return encode_token(data, expires_delta)

user_auth = UserAuthenticator(user_crud)

def encode_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWTError:
        admin_log.error("Failed to decode token.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials",)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            admin_log.warning("Token does not contain user ID.")
            raise credentials_exception

        user = await user_crud.get_user_by_id(int(user_id))
        if user is None:
            admin_log.warning(f"User with ID {user_id} not found in database.")
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
