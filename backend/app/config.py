import os
#from os import environ as env # Use in production

class Settings:

    # Project
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    VERSION = os.getenv('PROJECT_VERSION')

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = 60*1000 # Hours

    # FastAPI
    TOKEN_URL = "/user/login"

    # Database
    DB_NAME = os.getenv('DATABASE_NAME')
    DB_USERNAME = os.getenv('DATABASE_USERNAME')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_URL = os.getenv('DATABASE_URL')

settings = Settings()