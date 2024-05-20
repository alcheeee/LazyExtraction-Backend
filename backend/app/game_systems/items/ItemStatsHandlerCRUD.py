import tenacity
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.item_schema import ItemType, equipment_map, item_bonus_mapper
from ...crud import UserCRUD, UserInventoryCRUD
from ...models import (
    User,
    InventoryItem,
)


class ItemStatsHandler:
    def __init__(self, user_id: int, item_id: int, session: AsyncSession):
        self.user_id = user_id
        self.item_id = item_id
        self.session = session
        self.user_crud = UserCRUD(User, session)
        self.user_inventory_crud = UserInventoryCRUD(InventoryItem, session)

    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def user_equip_unequip_item(self):
        inventory, inventory_item, stats = await self.get_needed_info(self.item_id)

        item = inventory_item.item
        item_details = self.get_item_category(item)
        if not item_details:
            raise ValueError("Item details not available")

        item_slot_attr = self.determine_slot(item, item_details)
        if not item_slot_attr:
            raise ValueError("This item cannot be equipped")

        equipped_item_id = getattr(inventory, item_slot_attr)
        if equipped_item_id and equipped_item_id != item.id:
            await self.unequip_item(equipped_item_id, inventory, stats)

        if equipped_item_id == item.id:
            setattr(inventory, item_slot_attr, None)
            inventory_item.quantity += 1
            self.adjust_user_stats(stats, item_details, equip=False)
            status = "Item Unequipped"
        else:
            if inventory_item.quantity < 1:
                raise ValueError("Not enough quantity to equip")

            setattr(inventory, item_slot_attr, item.id)
            inventory_item.quantity -= 1
            self.adjust_user_stats(stats, item_details, equip=True)
            status = "Item Equipped"

        return status


    async def unequip_item(
            self,
            equipped_item_id: int,
            inventory=None,
            inventory_item=None,
            stats=None
    ):
        if inventory is None or inventory_item is None or stats is None:
            inventory, inventory_item, stats = await self.get_needed_info(equipped_item_id)

        item = inventory_item.item
        item_details = self.get_item_category(item)
        if not item_details:
            raise ValueError("Item details not available")

        item_slot_attr = self.determine_slot(item, item_details)
        if not item_slot_attr:
            raise ValueError("This item cannot be equipped")

        if inventory_item:
            setattr(inventory, item_slot_attr, None)
            inventory_item.quantity += 1
            self.adjust_user_stats(stats, item_details, equip=False)
            status = "Item Unequipped"
            return status


    async def get_needed_info(self, item_id: int):
        (
            inventory,
            stats,
            inventory_item
        ) = await self.user_inventory_crud.get_inv_stats_invitem(self.user_id, item_id)
        return inventory, inventory_item, stats


    def adjust_user_stats(self, stats, item_details, equip=True):
        """Adjust the users stats based on the item details"""
        multiplier = 1 if equip else -1
        for stat_key, attr_name in item_bonus_mapper.items():
            bonus_value = getattr(item_details, attr_name, 0)
            if bonus_value:
                current_value = getattr(stats, stat_key, 0)
                setattr(stats, stat_key, current_value + bonus_value * multiplier)
        stats.round_stats()

    def determine_slot(self, item, item_details):
        if item.category == ItemType.Clothing and hasattr(item_details, 'clothing_type'):
            return equipment_map.get(item_details.clothing_type)
        elif item.category == ItemType.Weapon:
            return equipment_map.get(ItemType.Weapon)
        return None

    def get_item_category(self, item):
        if item.category == ItemType.Clothing:
            return item.clothing_details
        elif item.category == ItemType.Weapon:
            return item.weapon_details
        return None

    def get_item_stats_json(self, item):
        item_stats_source = self.get_item_category(item)
        if not item_stats_source:
            return None

        item_stats_results = {}
        for stat_key, bonus_attr in item_bonus_mapper.items():
            item_bonus = getattr(item_stats_source, bonus_attr, 0)
            if item_bonus != 0 and item_bonus:
                item_stats_results[bonus_attr] = item_bonus
        return item_stats_results
