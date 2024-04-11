import secrets

class Settings:

    # Project
    PROJECT_NAME: str = "RPGapi | Development"
    VERSION: str = "0.1101"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # Database
    DB_NAME = "rpg_api"
    DB_USERNAME = "root"
    DB_PASSWORD = "root"
    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}"


settings = Settings()