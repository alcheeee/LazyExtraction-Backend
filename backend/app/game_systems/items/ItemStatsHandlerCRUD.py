from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from ...crud.UserCRUD import UserCRUD
from ...crud.UserInventoryCRUD import UserInventoryCRUD
from ...schemas.item_schema import ItemType, equipment_map, item_bonus_mapper
from ...models import (
    User,
    Stats,
    Inventory,
    InventoryItem,
    Items
)


class ItemStatsHandler:
    def __init__(self, user_id: int, item_id: int, session: AsyncSession):
        self.user_id = user_id
        self.item_id = item_id
        self.session = session
        self.user_crud = UserCRUD(User, session)
        self.user_inventory_crud = UserInventoryCRUD(InventoryItem, session)


    async def user_equip_unequip_item(self):
        try:
            result = await self.session.execute(
                select(
                    Inventory,
                    Stats,
                    InventoryItem
                ).select_from(User)
                 .join(Inventory, User.inventory_id == Inventory.id)
                 .join(InventoryItem, InventoryItem.inventory_id == Inventory.id)
                 .join(Stats, User.stats_id == Stats.id)
                 .where(User.id == self.user_id, InventoryItem.item_id == self.item_id)
                 .options(
                     selectinload(InventoryItem.item).joinedload(Items.clothing_details),
                     selectinload(InventoryItem.item).joinedload(Items.weapon_details)
                 )
            )
            inventory, stats, inventory_item = result.one()

        except Exception as e:
            raise e

        item = inventory_item.item
        item_details = self.get_item_category(item)
        if not item_details:
            raise ValueError("Item details not available")

        item_slot_attr = self.determine_slot(item, item_details)
        if not item_slot_attr:
            raise ValueError("Item type is not valid for equipping")

        current_equipped_item_id = getattr(inventory, item_slot_attr)

        if current_equipped_item_id == item.id:
            setattr(inventory, item_slot_attr, None)
            self.adjust_user_stats(stats, item_details, equip=False)
        else:
            setattr(inventory, item_slot_attr, item.id)
            self.adjust_user_stats(stats, item_details, equip=True)

        return "Equipped" if current_equipped_item_id != item.id else "Unequipped"


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


