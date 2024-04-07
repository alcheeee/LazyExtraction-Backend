from fastapi import FastAPI
from app.config import settings
from app.database.db import initialize_db
from app.routes.routes import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.VERSION
            )

    @app.on_event("startup")
    async def startup_event():
        initialize_db()

    app.include_router(user_router)
    return app


app = create_app()

r"""
To run app:

cd "C:\Users\romai\OneDrive\Documents\Python Projects\RPG API"
uvicorn app.main:app --reload

"""