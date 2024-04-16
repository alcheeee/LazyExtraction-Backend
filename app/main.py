from fastapi import FastAPI
from app.config import settings
from app.database.db import initialize_db, engine
from app.routes.routes import user_router
from app.routes.admin_routes import admin_router
from app.routes.corporation_routes import corporation_router
from app.routes.market_routes import market_router
from app.routes.game_routes import game_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.VERSION
            )

    @app.on_event("startup")
    async def startup_event():
        initialize_db()

    app.include_router(user_router)
    app.include_router(game_router)
    app.include_router(corporation_router)
    app.include_router(market_router)
    app.include_router(admin_router)
    return app


app = create_app()

