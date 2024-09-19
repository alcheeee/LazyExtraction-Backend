from contextlib import asynccontextmanager

import anyio
from fastapi import FastAPI

from .config import settings
from .database.db import sessionmanager, init_game_content
from .routes import (
    user_router,
    admin_router,
    crew_router,
    market_router,
    game_router,
    info_router,
    combat_router,
    inventory_router
)


def init_app(init_db=True) -> FastAPI:
    lifespan = None

    if init_db:
        sessionmanager.init(settings.DB_CONFIG)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await init_game_content()
            limiter = anyio.to_thread.current_default_thread_limiter()
            limiter.total_tokens = 40
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    server = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
    )
    server.include_router(user_router)
    server.include_router(info_router)
    server.include_router(inventory_router)
    server.include_router(game_router)
    server.include_router(combat_router)
    server.include_router(crew_router)
    server.include_router(market_router)
    server.include_router(admin_router)


    return server
