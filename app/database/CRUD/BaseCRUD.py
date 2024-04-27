from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound
from app.models.models import User, InventoryItem, Inventory, Stats

class BaseCRUD:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id, options=None):
        """Fetch an instance by its ID, potentially with sqlalchemy eager loading options."""
        query = select(self.model).where(self.model.id == id)
        if options:
            for option in options:
                query = query.options(option)
        result = await self.session.execute(query)
        instance = result.scalar()
        if not instance:
            raise NoResultFound(f"No {self.model.__name__} found with ID: {id}")
        return instance

    async def create(self, **kwargs):
        """Create a new instance of the model."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def update(self, id, **kwargs):
        """Update an existing instance."""
        instance = await self.get_by_id(id)
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.commit()
        return instance

    async def delete(self, id):
        """Delete an instance by its ID."""
        instance = await self.get_by_id(id)
        await self.session.delete(instance)
        await self.session.commit()

class EnhancedCRUD(BaseCRUD):
    async def get_by_id(self, id, options=None):
        query = select(self.model).where(self.model.id == id)
        if options:
            query = query.options(*options)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()
        return instance

    async def get_inventory_item_by_conditions(self, inventory_id, item_id):
        result = await self.session.execute(
            select(InventoryItem)
            .where(
                InventoryItem.inventory_id == inventory_id,
                InventoryItem.item_id == item_id
            )
        )
        return result.scalars().first()

    async def get_one(self, *criterion):
        """Fetch a single instance based on criteria."""
        query = select(self.model).where(*criterion)
        result = await self.session.execute(query)
        return result.scalars().first()