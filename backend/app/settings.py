import os
from fastapi.security import OAuth2PasswordBearer


class Settings:
    # FastAPI
    TOKEN_URL = "/user/login"
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    VERSION = os.getenv('PROJECT_VERSION')

    TESTING = False  # DANGEROUS! WIPES DATABASE

    # Database
    SHOULD_ECHO = False

    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "supersecretdatabasepassword")
    DB_NAME = os.getenv("DB_NAME", "LazyExtractionAPI")
    DB_HOST = os.getenv("DB_HOST", "database")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Redis
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')
    redis_tte = 30

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 600 # TODO : Reduce this in production
    REFRESH_TOKEN_EXPIRE_DAYS = 100
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL) # Not implemented right now

    # Game setup variables
    GAME_BOT_USERNAME = os.getenv('GAME_BOT_USERNAME')
    GAME_BOT_PASSWORD = os.getenv('GAME_BOT_PASSWORD')
    GAME_BOT_EMAIL = os.getenv('GAME_BOT_EMAIL')
    GAME_BOT_USER_ID = None


settings = Settings()
