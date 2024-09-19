import uuid

from typing import Annotated
from datetime import datetime, timedelta

from passlib.hash import argon2
from jose import jwt, exceptions
from ..config import settings

from ..utils import CommonHTTPErrors


class PasswordSecurity:
    @staticmethod
    async def hash_password(password: str) -> str:
        return argon2.using(time_cost=1, memory_cost=65536, parallelism=2).hash(password)

    @staticmethod
    async def check_pass_hash(password: str, hashed_password: str) -> bool:
        return argon2.verify(password, hashed_password)


class TokenHandler:

    @staticmethod
    def create_access_token(
            user_data: dict,
            expires_delta: timedelta | None = None,
            refresh: bool = False
    ) -> str:
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "user": user_data,
            "refresh": refresh
        }

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            token_data = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return token_data
        except exceptions.ExpiredSignatureError as e:
            raise CommonHTTPErrors.credentials_error("Session expired, please re-login", exception=str(e))
        except jwt.JWTError as e:
            raise CommonHTTPErrors.credentials_error(exception=str(e))
