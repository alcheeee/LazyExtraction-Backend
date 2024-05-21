from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class ItemType(str, Enum):
    Drug = "Drug"
    Weapon = "Weapon"
    Armor = "Armor"
    Clothing = "Clothing"
    Other = "Other"

class ClothingType(str, Enum):
    Mask = "Mask"
    Body = "Body"
    Legs = "Legs"

class ArmorType(str, Enum):
    Head = "Head"
    Body = "Body"

class ItemTier(Enum):
    Tier1 = 'Tier 1'
    Tier2 = 'Tier 2'
    Tier3 = 'Tier 3'
    Tier4 = 'Tier 4'
    Tier5 = 'Tier 5'
    Tier6 = 'Tier 6'

equipment_map = {
    ItemType.Weapon: "equipped_weapon_id",
    ClothingType.Mask: "equipped_mask_id",
    ClothingType.Body: "equipped_body_id",
    ClothingType.Legs: "equipped_legs_id",
    ArmorType.Head: "equipped_head_armor_id",
    ArmorType.Body: "equipped_body_armor_id",
}

clothing_bonus_wrapper = {
    "reputation": "reputation_bonus",
    "max_energy": "max_energy_bonus",
    "agility": "agility_bonus",
    "health": "health_bonus",
    "luck": "luck_bonus",
    "strength": "strength_bonus",
    "knowledge": "knowledge_bonus",
}

armor_bonus_wrapper = {
    "head_protection": "head_protection",
    "chest_protection": "chest_protection",
    "stomach_protection": "stomach_protection",
    "arm_protection": "arm_protection",
    "agility": "agility_penalty"
}

weapon_bonus_wrapper = {
    "strength": "strength_bonus",
    "damage": "damage_bonus",
    "agility": "agility_penalty"
}

class ItemCreate(BaseModel):
    item_name: str = "AR"
    quality: ItemTier = ItemTier.Tier1
    quick_sell: int = 10
    category: ItemType = ItemType.Weapon
    illegal: bool = False
    randomize_all: bool = False
    randomize_stats: bool = False


class ClothingCreate(ItemCreate):
    clothing_type: Optional[ClothingType]
    reputation_bonus: Optional[int] = 0
    max_energy_bonus: Optional[int] = 0
    damage_bonus: Optional[int] = 0
    agility_bonus: Optional[float] = 0.01
    health_bonus: Optional[int] = 0
    luck_bonus: Optional[float] = 0.01
    strength_bonus: Optional[float] = 0.01
    knowledge_bonus: Optional[float] = 0.01

class WeaponCreate(ItemCreate):
    weight: float = 3.5
    max_durability: int = 100
    current_durability: float = 100.00

    damage_bonus: int = 0
    strength_bonus: float = 0.01
    range: int = 5
    accuracy: int = 50
    reload_speed: float = 2.5
    fire_rate: float = 2.2
    magazine_size: int = 0
    armor_penetration: int = 0
    headshot_chance: int = 0
    agility_penalty: float = -1.4

class ArmorCreate(ItemCreate):
    type: ArmorType = ArmorType.Head
    max_durability: int = 100
    current_durability: float = 100.00
    weight: float = 5.5

    head_protection: int = 0
    chest_protection: int = 0
    stomach_protection: int = 0
    arm_protection: int = 0
    agility_penalty: float = -0.4


class FilterItemStats:

    class ClothingStats(Enum):
        CLOTHING_TYPE = "clothing_type"
        REPUTATION_BONUS = "reputation_bonus"
        MAX_ENERGY_BONUS = "max_energy_bonus"
        DAMAGE_BONUS = "damage_bonus"
        AGILITY_BONUS = "agility_bonus"
        HEALTH_BONUS = "health_bonus"
        LUCK_BONUS = "luck_bonus"
        STRENGTH_BONUS = "strength_bonus"
        KNOWLEDGE_BONUS = "knowledge_bonus"

    class WeaponStats(Enum):
        DAMAGE_BONUS = "damage_bonus"
        STRENGTH_BONUS = "strength_bonus"
        WEIGHT = "weight"
        DURABILITY = "durability"
        RANGE = "range"
        ACCURACY = "accuracy"
        RELOAD_SPEED = "reload_speed"
        FIRE_RATE = "fire_rate"
        MAGAZINE_SIZE = "magazine_size"
        ARMOR_PENETRATION = "armor_penetration"
        HEADSHOT_CHANCE = "headshot_chance"
        AGILITY_PENALTY = "agility_penalty"

    class ArmorStats(Enum):
        TYPE = "type"
        DURABILITY = "durability"
        WEIGHT = "weight"
        HEAD_PROTECTION = "head_protection"
        CHEST_PROTECTION = "chest_protection"
        STOMACH_PROTECTION = "stomach_protection"
        ARM_PROTECTION = "arm_protection"
        AGILITY_PENALTY = "agility_penalty"

    def list(self, item_class: Enum) -> List[str]:
        return [stat.value for stat in item_class]

    def get_relevant_stats(self, category: ItemType) -> List[str]:
        if category == ItemType.Clothing:
            return self.list(self.ClothingStats)
        elif category == ItemType.Weapon:
            return self.list(self.WeaponStats)
        elif category == ItemType.Armor:
            return self.list(self.ArmorStats)
        return []

filter_item_stats = FilterItemStats()