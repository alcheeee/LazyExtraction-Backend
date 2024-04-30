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
    echo=True,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=100,
    max_overflow=0,
    pool_recycle=30
)

async_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    if settings.PROJECT_MODE == settings.Mode.development:
        async with get_session() as session:
            await init_jobs_content(session)


