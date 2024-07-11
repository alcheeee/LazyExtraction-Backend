import os


class Settings:

    # FastAPI
    TOKEN_URL = "/user/login"
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    VERSION = os.getenv('PROJECT_VERSION')

    # Redis
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')
    redis_tte = 30

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # Database
    TESTING = True
    SHOULD_ECHO = False
    DATABASE_URL = os.getenv('DATABASE_URL')


    # Game setup variables
    # Setup later
    GAME_BOT_USERNAME = 'Game Admin'
    GAME_MARKET_USERNAME = 'Market'


settings = Settings()