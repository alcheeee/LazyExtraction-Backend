from sqlalchemy import select
from .BaseCRUD import BaseCRUD
from ..models.models import InventoryItem


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

