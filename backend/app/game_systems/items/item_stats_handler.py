from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import UserCRUD, UserInventoryCRUD
from . import (
    ItemType,
    ArmorType,
    ClothingType
)
from app.models import (
    User,
    InventoryItem,
    Clothing,
    Armor,
    Weapon,
    Inventory,
    Stats,
    Items
)
from app import globals


class ItemStatsHandler:

    def __init__(self, user_id: int, inventory_item_id: int, session: AsyncSession):
        self.user_id = user_id
        self.inventory_item_id = inventory_item_id
        self.session = session
        self.user_crud = UserCRUD(User, session)
        self.user_inventory_crud = UserInventoryCRUD(InventoryItem, session)
        self.user = None
        self.stats = None
        self.inventory = None

    async def equip_item(self) -> dict:
        data_to_return = {}
        user, inventory, stats, inventory_item = await self.get_user_data()
        item, item_details = await self.get_item_data(inventory_item)
        item_slot_attr = self.determine_slot(item, item_details)

        if inventory_item.amount_in_inventory < 1:
            raise ValueError("Item not found in inventory")

        if not item_slot_attr:
            raise ValueError("This item cannot be equipped")

        if inventory_item.one_equipped:
            raise ValueError("Item is already equipped")

        equipped_item_id = getattr(inventory, item_slot_attr)
        if equipped_item_id:
            unequipped_item = await self.unequip_item(equipped_item_id, called_from_equip=True)
            data_to_return['unequipped-item'] = unequipped_item

        await self.update_equipped_status(inventory, item_slot_attr, inventory_item, True)
        await self.adjust_user_stats(stats, item_details, equip=True)

        data_to_return['stats'] = stats
        data_to_return['user-inventory'] = inventory
        data_to_return['equipped-item'] = inventory_item
        return data_to_return

    async def unequip_item(
            self, inventory_item_id: Optional[int] = None, called_from_equip: bool = False
    ) -> dict | InventoryItem:
        if inventory_item_id is None:
            inventory_item_id = self.inventory_item_id

        user, inventory, stats, inventory_item = await self.get_user_data(inventory_item_id)
        item, item_details = await self.get_item_data(inventory_item)
        item_slot_attr = self.determine_slot(item, item_details)

        if not item_slot_attr:
            raise ValueError("This item cannot be equipped")

        if not inventory_item.one_equipped:
            raise ValueError("Item is not equipped")

        await self.update_equipped_status(inventory, item_slot_attr, inventory_item, False)
        await self.adjust_user_stats(stats, item_details, equip=False)

        if called_from_equip:
            return inventory_item

        data_to_return = {
            'stats': stats,
            'user-inventory': inventory,
            'unequipped-item': inventory_item
        }
        return data_to_return

    async def get_user_data(
            self, inventory_item_id: Optional[int] = None
    ) -> tuple[User, Inventory, Stats, InventoryItem]:

        item_id = inventory_item_id or self.inventory_item_id
        inventory_item = await self.user_inventory_crud.get_inventory_item_by_userid(
            self.user_id, item_id
        )
        if not inventory_item:
            raise LookupError("Item not found in inventory")

        if None not in [self.user, self.inventory, self.stats]:
            return self.user, self.inventory, self.stats, inventory_item

        user = await self.session.get(User, self.user_id)
        if not user:
            raise LookupError("User not found")

        inventory = await self.session.get(Inventory, user.inventory_id)
        stats = await self.session.get(Stats, user.stats_id)

        self.user = user
        self.inventory = inventory
        self.stats = stats
        return user, inventory, stats, inventory_item  # type: ignore

    async def get_item_data(
            self, inventory_item: InventoryItem
    ) -> tuple[Items, Clothing | Weapon | Armor]:

        item = await self.session.get(Items, inventory_item.item_id)
        if not item:
            raise LookupError("Item not found")

        item_details = await self.get_item_details(item)  # type: ignore
        if not item_details:
            raise LookupError("Item details not available")

        return item, item_details  # type: ignore

    async def update_equipped_status(
            self, inventory: Inventory,
            item_slot_attr: str,
            inventory_item: InventoryItem,
            equip: bool
    ) -> None:
        if equip:
            setattr(inventory, item_slot_attr, inventory_item.id)
            inventory_item.one_equipped = True
            inventory_item.amount_in_inventory -= 1
        else:
            setattr(inventory, item_slot_attr, None)
            inventory_item.one_equipped = False
            inventory_item.amount_in_inventory += 1

        await self.session.flush()

    async def adjust_user_stats(
            self,
            stats: Stats,
            item_details: Clothing | Weapon | Armor,
            equip: bool = True
    ):
        multiplier = 1 if equip else -1
        adj_wrapper = self.get_adj_wrapper(item_details)

        for stat_key, attr_name in adj_wrapper.items():
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
    def get_adj_wrapper(item_details: Clothing | Weapon | Armor):
        if isinstance(item_details, Clothing):
            return {
                "reputation": "reputation_adj",
                "max_energy": "max_energy_adj",
                "agility": "agility_adj",
                "health": "health_adj",
                "luck": "luck_adj",
                "strength": "strength_adj",
                "knowledge": "knowledge_adj",
            }
        elif isinstance(item_details, Armor):
            return {
                "head_protection": "head_protection_adj",
                "chest_protection": "chest_protection_adj",
                "stomach_protection": "stomach_protection_adj",
                "arm_protection": "arm_protection_adj",
                "agility": "agility_adj"
            }
        elif isinstance(item_details, Weapon):
            return {
                "damage": "damage",
                "strength": "strength_adj",
                "agility": "agility_adj"
            }
        return {}

    async def get_item_details(self, item: Items):
        await self.session.refresh(item, ["clothing_details", "weapon_details", "armor_details"])
        match item.category:
            case ItemType.Clothing:
                return item.clothing_details
            case ItemType.Weapon:
                return item.weapon_details
            case ItemType.Armor:
                return item.armor_details
            case _:
                return None



