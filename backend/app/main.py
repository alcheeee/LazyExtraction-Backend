from contextlib import asynccontextmanager

import anyio
from fastapi import FastAPI
from app.settings import settings
from app.database.redis_handler import redis_client
from app.database.db import sessionmanager, init_game_content

from app.routes.game_routes import game_router
from app.routes.admin_routes import admin_router
from app.routes.crew_routes import crew_router
from app.routes.auth_routes import user_router
from app.routes.game_routes import game_router
from app.routes.market_routes import market_router
from app.routes.inventory_routes import inventory_router
from app.routes.combat_routes import combat_router
from app.routes.user_info_routes import info_router


def init_app(init_db=True) -> FastAPI:
    lifespan = None

    if init_db:
        sessionmanager.init(settings.DB_URI)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await init_game_content()
            await redis_client.init()

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
