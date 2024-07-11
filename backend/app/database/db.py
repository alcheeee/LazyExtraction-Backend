from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sqlalchemy
from sqlmodel import SQLModel
from fastapi import Depends

from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from .init_db import init_content
from ..config import settings



engine = create_async_engine(
    url=settings.DATABASE_URL,
    isolation_level="REPEATABLE READ",
    echo=settings.SHOULD_ECHO,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=30,
    max_overflow=10,
    pool_recycle=300
)

async_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        await session.close()


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.close()


async def init_db():
    if settings.TESTING:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with get_session() as session:
        await init_content(session)
        await session.commit()
