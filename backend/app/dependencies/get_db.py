from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import sessionmanager


async def get_db() -> AsyncSession:
    async with sessionmanager.session() as session:
        yield session
