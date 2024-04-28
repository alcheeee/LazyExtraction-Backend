from fastapi.security import OAuth2PasswordBearer
import bcrypt
from ..config import settings

SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)