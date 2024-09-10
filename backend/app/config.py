import os
from fastapi.security import OAuth2PasswordBearer


class Settings:

    TESTING = True # DANGEROUS! WIPES DATABASE


    # FastAPI
    TOKEN_URL = "/user/login"
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    VERSION = os.getenv('PROJECT_VERSION')

    # Redis
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')
    redis_tte = 30

    # Security
    REFRESH_TOKEN_SECRET_KEY = os.getenv('REFRESH_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    REFRESH_TOKEN_EXPIRE_DAYS = 100
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

    # Database
    SHOULD_ECHO = False
    DATABASE_URL = os.getenv('DATABASE_URL')

    # Game setup variables
    GAME_BOT_USERNAME = os.getenv('GAME_BOT_USERNAME')
    GAME_BOT_PASSWORD = os.getenv('GAME_BOT_PASSWORD')
    GAME_BOT_EMAIL = os.getenv('GAME_BOT_EMAIL')
    GAME_BOT_USER_ID = None


settings = Settings()