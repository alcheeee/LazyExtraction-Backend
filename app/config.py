import secrets

class Settings:

    # Project
    PROJECT_NAME: str = "RPGapi | Development"
    VERSION: str = "0.1091"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # Database
    SQLITE_URL = f"sqlite:///app/database.db"

settings = Settings()