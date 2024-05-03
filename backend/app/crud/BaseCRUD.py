from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound


class BaseCRUD:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id, options=None):
        """Get an instance by its id"""
        query = select(self.model).where(self.model.id == id)
        if options:
            query = query.options(*options)
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

    async def get_fields(self, id, *fields):
        """Get specific fields of a model by id"""
        if not fields:
            raise ValueError("No fields specified for retrieval.")

        model_fields = {field.name for field in self.model.__table__.columns}
        requested_fields = set(fields)
        if not requested_fields.issubset(model_fields):
            missing_fields = requested_fields - model_fields
            raise ValueError(f"Invalid field names: {', '.join(missing_fields)}")

        query = (select([getattr(self.model, field) for field in fields])
                 .where(self.model.id == id).options(load_only(*fields)))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def exists_by_id(self, id):
        """Check if a record exists by id"""
        query = select([1]).where(self.model.id == id).limit(1)
        result = await self.session.execute(query)
        return result.scalar() is not None







