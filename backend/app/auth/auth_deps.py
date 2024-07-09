from .auth_bearer import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from passlib.hash import argon2
from jose import jwt
from ..database import redis_client


class PasswordSecurity:
    @staticmethod
    async def hash_password(password: str) -> str:
        return argon2.using(time_cost=1, memory_cost=65536, parallelism=2).hash(password)

    @staticmethod
    async def check_pass_hash(password: str, hashed_password: str) -> bool:
        return argon2.verify(password, hashed_password)


class TokenHandler:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = 'HS256'
        self.expiry_minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    def _create_token_payload(self, user_id: int) -> dict:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expiry_minutes)
        return {"sub": str(user_id), "exp": expire}

    async def create_token(self, user_id: int) -> str:
        payload = self._create_token_payload(user_id)
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    async def decode_token(self, token: str) -> dict:
        cached_payload = await redis_client.get_cache(f"token:{token}")
        if cached_payload:
            return cached_payload
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            await redis_client.set_cache(f"token:{token}", payload, expire=self.expiry_minutes)
            return payload
        except jwt.JWTError:
            raise ValueError("Could not validate login")


token_handler = TokenHandler()
