from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import AsyncAdaptedQueuePool
from .init_db.init_jobs import init_jobs_content
from ..config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    echo=True,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=10,
    max_overflow=10
)

async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    if settings.PROJECT_MODE == settings.Mode.development:
        async with get_session() as session:
            await init_jobs_content(session)


