from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import jwt
from .auth_bearer import SECRET_KEY, ALGORITHM, pwd_context, oauth2_scheme
from Utils.logger import setup_logging
from ..database.UserCRUD import user_data_manager

class UserAuthenticator:
    def __init__(self, user_data_manager):
        self.user_data_manager = user_data_manager


    def get_user(self, db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)

    def authenticate_user(self, username: str, password: str):
        user = self.user_data_manager.get_user_by_username(username)
        if not user or not pwd_context.verify(password, user.password):
            return False
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


async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = user_data_manager.get_user_by_id(user_id)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
