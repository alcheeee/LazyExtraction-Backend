from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class ItemType(str, Enum):
    Drug = "Drug"
    Weapon = "Weapon"
    Clothing = "Clothing"
    Other = "Other"

class ClothingType(str, Enum):
    Mask = "Mask"
    Body = "Body"
    Legs = "Legs"

class ItemQuality(Enum):
    Junk = 'Junk'
    Common = 'Common'
    Uncommon = 'Uncommon'
    Rare = 'Rare'
    Special = 'Special'
    Unique = 'Unique'

equipment_map = {
    ItemType.Weapon: "equipped_weapon_id",
    ClothingType.Mask: "equipped_mask_id",
    ClothingType.Body: "equipped_body_id",
    ClothingType.Legs: "equipped_legs_id"
}


item_bonus_mapper = {
    "reputation": "reputation_bonus",
    "max_energy": "max_energy_bonus",
    "damage": "damage_bonus",
    "evasiveness": "evasiveness_bonus",
    "health": "health_bonus",
    "luck": "luck_bonus",
    "strength": "strength_bonus",
    "knowledge": "knowledge_bonus",
}

class MarketItemAdd(BaseModel):
    item_id: int
    market_name: str
    item_cost: int
    sell_price: int

class ItemCreate(BaseModel):
    item_name: str = "Bandana"
    quantity: int = 10
    illegal: bool = False
    category: ItemType
    randomize_all: bool = True
    randomize_stats: bool = False
    quality: ItemQuality

class ItemStats(ItemCreate):
    clothing_type: Optional[ClothingType]
    reputation_bonus: Optional[int]
    max_energy_bonus: Optional[int]
    damage_bonus: Optional[int]
    evasiveness_bonus: Optional[float]
    health_bonus: Optional[int]
    luck_bonus: Optional[float]
    strength_bonus: Optional[float]
    knowledge_bonus: Optional[float]


class FilterItemStats:
    class WeaponStats(Enum):
        DAMAGE_BONUS = "damage_bonus"
        STRENGTH_BONUS = "strength_bonus"
        EVASIVENESS_BONUS = "evasiveness_bonus"

    class ClothingStats(Enum):
        REPUTATION_BONUS = "reputation_bonus"
        MAX_ENERGY_BONUS = "max_energy_bonus"
        EVASIVENESS_BONUS = "evasiveness_bonus"
        HEALTH_BONUS = "health_bonus"
        STRENGTH_BONUS = "strength_bonus"
        KNOWLEDGE_BONUS = "knowledge_bonus"


    def list(self, item_class: Enum) -> List[str]:
        return [stat.value for stat in item_class]

    def get_relevant_stats(self, category: ItemType) -> List[str]:
        if category == ItemType.Weapon:
            return self.list(self.WeaponStats)
        elif category == ItemType.Clothing:
            return self.list(self.ClothingStats)
        return []
filter_item_stats = FilterItemStats()