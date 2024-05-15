from sqlmodel import SQLModel
from fastapi import Depends
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.pool import AsyncAdaptedQueuePool
from .init_db.init_jobs import init_jobs_content
from ..config import settings
from ..utils.logger import MyLogger
error_log = MyLogger.errors()


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=30,
    max_overflow=10,
    pool_recycle=1800
)

async_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def dependency_session() -> Depends(AsyncSession):
    db_session = async_session()
    try:
        yield db_session
    finally:
        await db_session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    if settings.PROJECT_MODE == settings.Mode.development:
        async with get_session() as session:
            await init_jobs_content(session)


