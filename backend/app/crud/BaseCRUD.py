from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound


class BaseCRUD:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def execute_scalar_one_or_none(self, query):
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, id, options=None):
        """Get an instance by its id"""
        query = select(self.model).where(self.model.id == id)
        if options:
            query = query.options(*options)
        return await self.execute_scalar_one_or_none(query)

    async def check_fields_exist(self, **conditions):
        """Check if a record exists."""
        if not conditions:
            return False
        query_conditions = [getattr(self.model, field) == value for field, value in conditions.items()]
        exists_query = select(self.model.id).where(or_(*query_conditions)).limit(1)
        result = await self.session.execute(exists_query)
        return result.scalar() is not None






