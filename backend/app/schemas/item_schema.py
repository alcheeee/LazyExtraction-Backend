from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class ItemType(str, Enum):
    Medical = "Medical"
    Armor = "Armor"
    Clothing = "Clothing"
    Weapon = "Weapon"
    Bullets = "Bullets"
    Attachments = "Attachments"
    Valuable = "Valuable"

class ClothingType(str, Enum):
    Mask = "Mask"
    Shirt = "Shirt"
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

tier_weights = {
    # Second value is supposed to be Luck Factor, not added yet
    ItemTier.Tier1: (60, 1),
    ItemTier.Tier2: (40, 2),
    ItemTier.Tier3: (35, 3),
    ItemTier.Tier4: (10, 4),
    ItemTier.Tier5: (3, 5),
    ItemTier.Tier6: (1, 6)
}

tier_multipliers = {
    ItemTier.Tier1: 1,
    ItemTier.Tier2: 1.25,
    ItemTier.Tier3: 1.5,
    ItemTier.Tier4: 2,
    ItemTier.Tier5: 2.5,
    ItemTier.Tier6: 3
}

equipment_map = {
    ItemType.Weapon: "equipped_weapon_id",
    ClothingType.Mask: "equipped_mask_id",
    ClothingType.Shirt: "equipped_body_id",
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

medical_bonus_wrapper = {
    "max_weight": "weight_bonus",
    "agility": "agility_bonus"
}


class ItemCreate(BaseModel):
    item_name: str = "AR"
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 10
    category: ItemType = ItemType.Weapon
    randomize_all: bool = False
    randomize_stats: bool = False
    texture: Optional[str] = None


class MedicalCreate(ItemCreate):
    health_increase: int = 0
    pain_reduction: int = 0
    weight_bonus: int = 0
    agility_bonus: int = 0
    amount_of_actions: int = 1


class ClothingCreate(ItemCreate):
    clothing_type: Optional[ClothingType]
    reputation_bonus: Optional[int] = 0
    max_energy_bonus: Optional[int] = 0
    agility_bonus: Optional[float] = 0.00
    health_bonus: Optional[int] = 0
    strength_bonus: Optional[float] = 0.00
    knowledge_bonus: Optional[float] = 0.00
    luck_bonus: Optional[float] = 0.00


class ArmorCreate(ItemCreate):
    type: ArmorType = ArmorType.Head
    max_durability: int = 100
    current_durability: float = 100.00
    weight: float = 0.0
    head_protection: int = 0
    chest_protection: int = 0
    stomach_protection: int = 0
    arm_protection: int = 0
    agility_penalty: float = -0.0


class FilterItemStats:
    class MedicalStats(Enum):
        HEALTH_INCREASE = "health_increase"
        PAIN_REDUCTION = "pain_reduction"
        WEIGHT_BONUS = "weight_bonus"
        AGILITY_BONUS ="agility_bonus"
        AMOUNT_OF_ACTIONS = "amount_of_actions"

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
        DAMAGE = "damage"
        STRENGTH = "strength"
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