from sqlalchemy import select
from .BaseCRUD import BaseCRUD
from ..models.models import InventoryItem, User


class UserCRUD(BaseCRUD):
    async def get_inventory_item_by_conditions(self, inventory_id, item_id):
        result = await self.session.execute(
            select(InventoryItem)
            .where(
                InventoryItem.inventory_id == inventory_id,
                InventoryItem.item_id == item_id
            )
        )
        return result.scalars().first()

    async def is_user_admin(self, user_id: int):
        result = await self.session.execute(
            select(User.is_admin, User.username).where(User.id == user_id)
        )
        user_data = result.first()
        if user_data:
            is_admin, username = user_data
            return username if is_admin else False
        return False
