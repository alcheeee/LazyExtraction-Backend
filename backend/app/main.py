from fastapi import FastAPI
from .config import settings
from .database.db import init_db
from .routes import (
    user_router,
    admin_router,
    corporation_router,
    market_router,
    game_router,
    user_info_router,
    social_router
)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

    app.include_router(user_router)
    app.include_router(user_info_router)
    app.include_router(corporation_router)
    app.include_router(social_router)
    app.include_router(game_router)
    app.include_router(market_router)
    app.include_router(admin_router)

    return app

async def startup():
    await init_db()


app = create_app()
app.router.on_startup.append(startup)


