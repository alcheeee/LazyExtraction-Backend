import secrets

class Settings:

    # Project
    PROJECT_NAME = "RPGapi | Development"
    VERSION = "0.1216"

    # Security
    SECRET_KEY = "nyasawesomehonestlyidontthinktheresanyonebetter"
    ACCESS_TOKEN_EXPIRE_MINUTES = 3000000
    ITEMS_SECRET_KEY = "itemsmmmyesitemsilovethose"

    # FastAPI
    TOKEN_URL = "/user/login"

    # Univorn
    HOST = "127.0.0.1"
    PORT = 8000

    # Database
    DB_NAME = "GameAPI"
    DB_USERNAME = "postgres"
    DB_PASSWORD = "root"
    DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}"


settings = Settings()