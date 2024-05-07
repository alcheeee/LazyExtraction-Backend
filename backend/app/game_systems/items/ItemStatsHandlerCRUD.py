from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from ...crud.UserCRUD import UserCRUD
from ...crud.ItemCRUD import ItemsCRUD
from ...crud.UserInventoryCRUD import UserInventoryCRUD
from ...schemas.item_schema import ItemType, equipment_map, item_bonus_mapper
from ...models.item_models import Items, Clothing
from ...models.models import User, InventoryItem
from ...utils.logger import MyLogger
error_log = MyLogger.errors()


class ItemStatsHandler:
    def __init__(self, user_id, item_id: int, session: AsyncSession):
        self.user_id = user_id
        self.item_id = item_id
        self.session = session
        self.user_crud = UserCRUD(User, session)
        self.user_inventory_crud = UserInventoryCRUD(InventoryItem, session)


    async def user_equip_unequip_item(self):
        user = await self.user_crud.get_by_id(self.user_id, options=[
            selectinload(User.inventory)
        ])
        item = await self.user_inventory_crud.get_by_id(self.item_id, options=[
            joinedload(Items.clothing_details),
            joinedload(Items.weapon_details)
        ])

        if not item or not user:
            raise ValueError("User or Item not found")

        item_details = self.get_item_category(item)
        if not item_details:
            raise ValueError("Item details not available")

        item_slot_attr = self.determine_slot(item, item_details)
        if not item_slot_attr:
            raise ValueError("Item type is not valid for equipping")

        current_equipped_item_id = getattr(user.inventory, item_slot_attr, None)

        if current_equipped_item_id == item.id:
            setattr(user.inventory, item_slot_attr, None)
            self.adjust_user_stats(user.stats, item_details, equip=False)
        else:
            setattr(user.inventory, item_slot_attr, item.id)
            if current_equipped_item_id:
                prev_item = await self.user_inventory_crud.get_by_id(current_equipped_item_id)
                prev_details = self.get_item_category(prev_item)
                self.adjust_user_stats(user.stats, prev_details, equip=False)
            self.adjust_user_stats(user.stats, item_details, equip=True)
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


