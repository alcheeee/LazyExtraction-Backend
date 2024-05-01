from .auth_bearer import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from jose import jwt
import asyncio
import bcrypt

executor = ThreadPoolExecutor()

class PasswordSecurity:
    async def hash_password(self, password):
        loop = asyncio.get_running_loop()
        hashed_password = await loop.run_in_executor(executor, bcrypt.hashpw,
                                                     password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    async def check_pass_hash(self, password, hashed_password):
        loop = asyncio.get_running_loop()
        check_hash = await loop.run_in_executor(executor, bcrypt.checkpw,
                                                password.encode('utf-8'),
                                                hashed_password.encode('utf-8'))
        return check_hash

class TokenHandler:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.algorithm = 'HS256'
        self.expiry_minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    def create_token(self, user_id: int):
        data = {"sub": str(user_id)}
        return self.encode_token(data)

    def encode_token(self, data: dict):
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expiry_minutes)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def decode_token(self, token: str):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.JWTError:
            raise ValueError("Could not validate login")


password_security = PasswordSecurity()
token_handler = TokenHandler(secret_key=SECRET_KEY)



