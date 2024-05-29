from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import (
    UserCRUD,
    UserInventoryCRUD,
    ItemsCRUD
)
from ..models.models import (
    User,
    Stats,
    Inventory,
    InventoryItem
)
from ..schemas import UserInfoNeeded


class GetUserInfo:

    def __init__(self, option: UserInfoNeeded, user_id: int, session: AsyncSession):
        self.option = option
        self.user_id = user_id
        self.session = session
        self.user_crud = UserCRUD(User, session)
        self.inventory_crud = UserInventoryCRUD(Inventory, session)


    async def get_info(self):
        if self.option == UserInfoNeeded.Stats:
            return await self.get_user_stats()
        elif self.option == UserInfoNeeded.Inventory:
            return await self.get_user_inventory()
        elif self.option == UserInfoNeeded.InventoryItems:
            return await self.get_all_inventory_items()
        else:
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
        return inventory_items


