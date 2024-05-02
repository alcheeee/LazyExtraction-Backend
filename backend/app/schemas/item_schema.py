from enum import Enum
from typing import Optional
from pydantic import BaseModel


class ItemType(Enum):
    Drug = "Drug"
    Weapon = "Weapon"
    Clothing = "Clothing"
    Other = "Other"

class ItemQuality(Enum):
    Junk = 'Junk'
    Common = 'Common'
    Uncommon = 'Uncommon'
    Rare = 'Rare'
    Special = 'Special'
    Unique = 'Unique'

equipment_map = {
    "Weapon": "equipped_weapon_id",
    "Mask": "equipped_mask_id",
    "Body": "equipped_body_id",
    "Legs": "equipped_legs_id"
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
    item_name: str
    quantity: int
    illegal: bool
    category: ItemType
    quality: ItemQuality
    randomize_stats: bool = True


class WeaponDetailCreate(ItemCreate):
    damage_bonus: int
    evasiveness_bonus: Optional[float]
    strength_bonus: Optional[float]


class ClothingDetailCreate(ItemCreate):
    clothing_type: str
    reputation_bonus: Optional[int]
    max_energy_bonus: Optional[int]
    evasiveness_bonus: Optional[float]
    health_bonus: Optional[int]
    luck_bonus: Optional[float]
    strength_bonus: Optional[float]
    knowledge_bonus: Optional[float]
