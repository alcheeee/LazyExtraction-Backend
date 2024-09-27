from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import (
    UserCRUD,
    UserInventoryCRUD,
    ItemsCRUD
)
from app.models.models import (
    User,
    Stats,
    Inventory,
    InventoryItem
)
from app.schemas import UserInfoNeeded


class GetUserInfo:

    def __init__(self, option: UserInfoNeeded, user_id: int, session: AsyncSession):
        self.option = option
        self.user_id = user_id
        self.session = session
        self.user_crud = UserCRUD(User, session)
        self.inventory_crud = UserInventoryCRUD(Inventory, session)


    async def get_info(self):
        match self.option:
            case UserInfoNeeded.Stats:
                return await self.get_user_stats()
            case UserInfoNeeded.Inventory:
                return await self.get_user_inventory()
            case UserInfoNeeded.InventoryItems:
                return await self.get_all_inventory_items()
            case _:
                raise Exception("Invalid Getter request")

    async def get_user_stats(self):
        stats_id = await self.user_crud.get_user_field_from_id(self.user_id, 'stats_id')
        stats = await self.session.get(Stats, stats_id)
        return stats


    async def get_user_inventory(self):
        inventory_id = await self.user_crud.get_user_field_from_id(self.user_id, 'inventory_id')
        inventory = await self.session.get(Inventory, inventory_id)
        return inventory


    async def get_all_inventory_items(self):
        inventory_id = await self.user_crud.get_user_field_from_id(self.user_id, 'inventory_id')
        inventory_items = await self.inventory_crud.get_all_items_by_inventory_id(inventory_id)
        return [item for item in inventory_items if item in inventory_items]


