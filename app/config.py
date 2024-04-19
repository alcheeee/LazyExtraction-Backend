import secrets

class Settings:

    # Project
    PROJECT_NAME = "RPGapi | Development"
    VERSION = "0.1201"

    # Security
    SECRET_KEY = "nyasawesomehonestlyidontthinktheresanyonebetter"
    ACCESS_TOKEN_EXPIRE_MINUTES = 3000000
    ITEMS_SECRET_KEY = "itemsmmmyesitemsilovethose"

    # FastAPI
    TOKEN_URL = "/user/login"

    # Database
    DB_NAME = "rpg_api"
    DB_USERNAME = "root"
    DB_PASSWORD = "root"
    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}"


settings = Settings()