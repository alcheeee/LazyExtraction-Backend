import tenacity
from sqlalchemy.ext.asyncio import AsyncSession
from ...crud import UserCRUD, UserInventoryCRUD
from . import (
    ItemType,
    equipment_map,
    clothing_bonus_wrapper,
    armor_bonus_wrapper,
    weapon_bonus_wrapper,
    ArmorType,
)
from ...models import (
    User,
    InventoryItem,
    Clothing,
    Armor,
    Weapon
)


class ItemStatsHandler:
    def __init__(self, user_id: int, item_id: int, session: AsyncSession):
        self.user_id = user_id
        self.item_id = item_id
        self.session = session
        self.user_crud = UserCRUD(User, session)
        self.user_inventory_crud = UserInventoryCRUD(InventoryItem, session)


    async def user_equip_unequip_item(self):
        inventory, inventory_item, stats = await self.get_needed_info(self.item_id)

        item = inventory_item.item
        item_details = self.get_item_details(item)
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
        item_details = self.get_item_details(item)
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
        bonus_wrapper = self.get_bonus_wrapper(item_details)

        for stat_key, attr_name in bonus_wrapper.items():
            bonus_value = getattr(item_details, attr_name, 0)
            if bonus_value:
                current_value = getattr(stats, stat_key, 0)
                setattr(stats, stat_key, current_value + bonus_value * multiplier)
        stats.round_stats()

    @staticmethod
    def determine_slot(item, item_details):
        if item.category == ItemType.Clothing and hasattr(item_details, 'clothing_type'):
            return equipment_map.get(item_details.clothing_type)
        elif item.category == ItemType.Weapon:
            return equipment_map.get(ItemType.Weapon)
        elif item.category == ItemType.Armor and hasattr(item_details, 'type'):
            if item_details.type == ArmorType.Head:
                return 'equipped_head_armor_id'
            elif item_details.type == ArmorType.Body:
                return 'equipped_body_armor_id'
        return None

    @staticmethod
    def get_bonus_wrapper(item_details):
        if isinstance(item_details, Clothing):
            return clothing_bonus_wrapper
        elif isinstance(item_details, Armor):
            return armor_bonus_wrapper
        elif isinstance(item_details, Weapon):
            return weapon_bonus_wrapper
        return {}

    @staticmethod
    def get_item_details(item):
        if item.category == ItemType.Clothing:
            return item.clothing_details
        elif item.category == ItemType.Weapon:
            return item.weapon_details
        elif item.category == ItemType.Armor:
            return item.armor_details
        return None

    def get_item_stats_json(self, item):
        item_details = self.get_item_details(item)
        if not item_details:
            return None

        bonus_wrapper = self.get_bonus_wrapper(item_details)
        item_stats_results = {}

        for stat_key, bonus_attr in bonus_wrapper.items():
            item_bonus = getattr(item_details, bonus_attr, 0)
            if item_bonus != 0 and item_bonus:
                item_stats_results[bonus_attr] = item_bonus
        return item_stats_results



