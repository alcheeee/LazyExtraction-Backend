from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound
from ..utils import RetryDecorators


class BaseCRUD:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session


    async def execute_scalar_one_or_none(self, query):
        """
        :param query: SQLAlchemy Statement
        :return: Optional[Result]
        """
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def check_fields_exist(self, **conditions):
        """Check if a record exists."""
        if not conditions:
            return False
        query_conditions = [getattr(self.model, field) == value for field, value in conditions.items()]
        exists_query = select(self.model.id).where(or_(*query_conditions)).limit(1)
        result = await self.session.execute(exists_query)
        return result.scalar() is not None






