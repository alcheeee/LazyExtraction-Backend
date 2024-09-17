import contextlib
from typing import AsyncGenerator, AsyncIterator

from fastapi import Depends

from sqlmodel import SQLModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from .redis_handler import redis_client
from .init_db import init_content, create_game_account
from ..config import settings


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(
            url=host,
            pool_size=30,
            max_overflow=10,
            pool_recycle=300,
            echo=settings.SHOULD_ECHO
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(SQLModel.metadata.create_all)
        await redis_client.clear_all_cached()

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(SQLModel.metadata.drop_all)
        await redis_client.clear_all_cached()


sessionmanager = DatabaseSessionManager()


async def get_db() -> AsyncSession:
    async with sessionmanager.session() as session:
        yield session


@contextlib.asynccontextmanager
async def get_session() -> AsyncSession:
    async with sessionmanager.session() as session:
        yield session


async def init_game_content():
    if settings.TESTING:
        async with sessionmanager.connect() as conn:
            await sessionmanager.drop_all(conn)
            await sessionmanager.create_all(conn)

    async with sessionmanager.session() as session:
        await init_content(session)
        await session.commit()

    async with sessionmanager.session() as session:
        await create_game_account(session)
        await session.commit()