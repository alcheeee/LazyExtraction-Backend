from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from .stats_crud import StatsCRUD
from app.models import (
    User,
    Inventory,
    InventoryItem,
    Stats,
    Items,
    Weapon,
    Bullets,
    Attachments
)
from .crud_utilities.inventory_items_util import (
    InventoryItemsCRUDUtils as InvItemUtils,
    AllowedArea
)


class WeaponCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_weapon(
            self, inventory_id: int, weapon_inventory_id: int
    ) -> tuple[Items, InventoryItem]:
        query = (
            select(InventoryItem)
            .join(Inventory, InventoryItem.inventory_id == Inventory.id)  # type: ignore
            .options(joinedload(InventoryItem.item).joinedload(Items.weapon_details))
            .where(InventoryItem.id == weapon_inventory_id)  # type: ignore
            .where(Inventory.id == inventory_id)
        )
        result = await self.session.execute(query)
        inventory_item = result.scalar_one_or_none()

        if not inventory_item or not inventory_item.item.weapon_details:
            raise LookupError("Weapon not found in inventory")

        return inventory_item.item, inventory_item


    async def update_weapon_for_attachments(
            self,
            user_id: int,
            weapon_inv_item: InventoryItem
    ) -> tuple[InventoryItem | None, InventoryItem]:
        if not weapon_inv_item:
            raise LookupError("Weapon inventory item not found")

        new_item = InventoryItem(
            item_name=weapon_inv_item.item_name,
            quick_sell_value=weapon_inv_item.quick_sell_value,
            inventory_id=weapon_inv_item.inventory_id,
            item_id=weapon_inv_item.item_id,
            is_modified=True,
            modifications=weapon_inv_item.modifications.copy() if weapon_inv_item.modifications else {},
            amount_in_stash=1,
            amount_in_inventory=0
        )

        self.session.add(new_item)
        await self.session.flush()

        new_inventory, new_stash = await InvItemUtils.amount_handler(
            weapon_inv_item, AllowedArea.ANY, -1
        )

        weapon_inv_item.amount_in_inventory = new_inventory
        weapon_inv_item.amount_in_stash = new_stash

        weight_change = InvItemUtils.calculate_weight_change(
            weapon_inv_item.item.weight, -1
        )

        stats_crud = StatsCRUD(self.session)
        await stats_crud.adjust_user_weight(user_id, weight_change)

        if new_inventory + new_stash == 0:
            await self.session.delete(weapon_inv_item)
            weapon_inv_item = None


        await self.session.flush()
        return new_item, weapon_inv_item



