from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Items
from app.crud.items_crud import ItemsCRUD

from .user_creator import create_users_with_related_entities
from .crew_creator import create_crews, assign_users_to_crews
from .inventory_creator import populate_user_inventories
from .market_listing_creator import create_market_items


class CreateTestData:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users_to_create = 10000
        self.crews_to_create = 1000
        self.market_listings = 15000


    async def create_mock_data(self):
        items_crud = ItemsCRUD(Items, self.session)
        items = await items_crud.get_all_items()
        users = await create_users_with_related_entities(self.session, self.users_to_create)
        crews = await create_crews(self.session, self.crews_to_create)

        await assign_users_to_crews(self.session, users, crews)
        await populate_user_inventories(self.session, users, items)
        await create_market_items(self.session, items, users, self.market_listings)
        await self.session.commit()


