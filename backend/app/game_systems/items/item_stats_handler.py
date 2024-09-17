from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from ...crud import UserCRUD, UserInventoryCRUD
from . import (
    ItemType,
    ArmorType,
    ClothingType
)
from ...models import (
    User,
    InventoryItem,
    Clothing,
    Armor,
    Weapon,
    Inventory,
    Stats,
    Items
)


class ItemStatsHandler:
    # TODO : Clean this mess up for new logic

    def __init__(self, user_id: int, inventory_item_id: int, session: AsyncSession):
        self.user_id = user_id
        self.inventory_item_id = inventory_item_id
        self.session = session
        self.user_crud = UserCRUD(User, session)
        self.user_inventory_crud = UserInventoryCRUD(InventoryItem, session)


    async def user_equip_unequip_item(self):
        inventory, inventory_item, stats = await self.get_needed_info()

        if not inventory_item:
            raise LookupError("Item not found in inventory")

        item = inventory_item.item
        item_details = self.get_item_details(item)
        if not item_details:
            raise LookupError("Item details not available")

        item_slot_attr = self.determine_slot(item, item_details)
        if not item_slot_attr:
            raise ValueError("This item cannot be equipped")

        equipped_item_id = getattr(inventory, item_slot_attr)
        if equipped_item_id and equipped_item_id != inventory_item.id:
            await self.unequip_item(equipped_item_id, inventory, stats)

        if equipped_item_id == inventory_item.id:
            setattr(inventory, item_slot_attr, None)
            inventory_item.amount_in_inventory += 1
            await self.adjust_user_stats(stats, item_details, equip=False)
            status = "Item Unequipped"
        else:
            if inventory_item.amount_in_inventory < 1:
                raise ValueError("You don't have that item in your inventory")

            setattr(inventory, item_slot_attr, inventory_item.id)
            inventory_item.amount_in_inventory -= 1
            await self.adjust_user_stats(stats, item_details, equip=True)
            status = "Item Equipped"

        return status


    async def unequip_item(
            self,
            equipped_inventory_item_id: int,
            inventory: Inventory,
            stats: Stats
    ):
        inventory_item = await self.session.get(InventoryItem, equipped_inventory_item_id)
        if not inventory_item:
            raise LookupError("Equipped item not found")

        item = inventory_item.item
        item_details = self.get_item_details(item)
        if not item_details:
            raise LookupError("Item details not available")

        item_slot_attr = self.determine_slot(item, item_details)
        if not item_slot_attr:
            raise ValueError("This item cannot be equipped")

        setattr(inventory, item_slot_attr, None)
        inventory_item.amount_in_inventory += 1
        await self.adjust_user_stats(stats, item_details, equip=False)


    async def get_needed_info(self):
        (inventory, stats, inventory_item) = (
            await self.user_inventory_crud.get_inv_stats_invitem(self.user_id, self.inventory_item_id)
        )
        return inventory, inventory_item, stats


    async def adjust_user_stats(
            self,
            stats: Stats,
            item_details: Union[Clothing, Weapon, Armor],
            equip: bool = True
    ):
        """Adjust the users stats based on the item details"""
        multiplier = 1 if equip else -1
        bonus_wrapper = self.get_bonus_wrapper(item_details)

        for stat_key, attr_name in bonus_wrapper.items():
            base_value = getattr(item_details, attr_name, 0)
            current_value = getattr(stats, stat_key, 0)
            setattr(stats, stat_key, current_value + base_value * multiplier)

        await stats.round_stats()

    @staticmethod
    def determine_slot(item: Items, item_details):
        equipment_map = {
            ItemType.Weapon: "equipped_weapon_id",
            ClothingType.Mask: "equipped_mask_id",
            ClothingType.Shirt: "equipped_body_id",
            ClothingType.Legs: "equipped_legs_id",
            ArmorType.Head: "equipped_head_armor_id",
            ArmorType.Body: "equipped_body_armor_id",
        }
        match item.category:
            case ItemType.Clothing:
                return equipment_map.get(item_details.clothing_type)
            case ItemType.Weapon:
                return equipment_map.get(ItemType.Weapon)
            case ItemType.Armor:
                return ('equipped_head_armor_id' if item_details.type == ArmorType.Head
                        else 'equipped_body_armor_id')
            case _:
                return None

    @staticmethod
    def get_bonus_wrapper(item_details: Union[Clothing, Weapon, Armor]):
        if isinstance(item_details, Clothing):
            return {
                "reputation": "reputation_bonus",
                "max_energy": "max_energy_bonus",
                "agility": "agility_bonus",
                "health": "health_bonus",
                "luck": "luck_bonus",
                "strength": "strength_bonus",
                "knowledge": "knowledge_bonus",
            }
        elif isinstance(item_details, Armor):
            return {
                "head_protection": "head_protection",
                "chest_protection": "chest_protection",
                "stomach_protection": "stomach_protection",
                "arm_protection": "arm_protection",
                "agility": "agility_penalty"
            }
        elif isinstance(item_details, Weapon):
            return {
                "strength": "strength",
                "agility": "agility_penalty"
            }
        return {}

    @staticmethod
    def get_item_details(item: Union[Clothing, Weapon, Armor, None]):
        match item.category:
            case ItemType.Clothing:
                return item.clothing_details

            case ItemType.Weapon:
                return item.weapon_details

            case ItemType.Armor:
                return item.armor_details

            case _:
                return None



