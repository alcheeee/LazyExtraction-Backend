import os
#from os import environ as env # Use in production

class Settings:
    class Mode:
        development = "Development"
        production = "Production"
        testing = "testing"

    PROJECT_MODE = Mode.development

    # FastAPI
    TOKEN_URL = "/user/login"
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    VERSION = os.getenv('PROJECT_VERSION')

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = 60*1000 # Hours

    # Database
    DB_NAME = os.getenv('DATABASE_NAME')
    DB_USERNAME = os.getenv('DATABASE_USERNAME')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_URL = os.getenv('DATABASE_URL')

    # Game setup variables
    # Setup later
    GAME_BOT_USERNAME = 'Game Admin'
    GAME_MARKET_USERNAME = 'Market'


settings = Settings()