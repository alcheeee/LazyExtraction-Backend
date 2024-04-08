from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from .auth_bearer import SECRET_KEY, ALGORITHM, pwd_context, oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES
from ..database.UserCRUD import user_crud
import logging
from ..utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)


class UserAuthenticator:
    def __init__(self, user_data_manager):
        self.user_data_manager = user_data_manager


    def authenticate_user(self, username: str, password: str):
        user = self.user_data_manager.get_user_by_username(username)
        if not user or not pwd_context.verify(password, user.password):
            logger.warning(f"User {username} failed login.")
            return False
        logger.info(f"User {username} logged in.")
        return user


    def create_access_token(self, user_id: int, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        data = {"sub": str(user_id)}
        return encode_token(data, expires_delta)


def encode_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",)


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
            raise credentials_exception

        user = user_crud.get_user_by_id(int(user_id))
        if user is None:
            logger.warning(f"User {user_id} not found.")
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
