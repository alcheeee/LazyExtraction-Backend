from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import (
    User,
    Inventory,
    InventoryItem,
    Stats,
    Items,
    Weapon,
    Bullets,
    Attachments,
    MarketItems,
    Market
)


class WeaponCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_weapon(self, user_id: int, weapon_inventory_id: int):
        query = (
            select(InventoryItem)
            .join(Inventory, InventoryItem.inventory_id == Inventory.id)
            .join(User, User.inventory_id == Inventory.id)
            .options(joinedload(InventoryItem.item).joinedload(Items.weapon_details))
            .where(InventoryItem.id == weapon_inventory_id)
            .where(User.id == user_id)
        )
        result = await self.session.execute(query)
        inventory_item = result.scalar_one_or_none()
        if not inventory_item or not inventory_item.item.weapon_details:
            raise LookupError("Weapon not found in user's inventory")

        return inventory_item.item, inventory_item
