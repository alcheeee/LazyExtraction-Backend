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


class StashStatusSwitch(BaseModel):
    item_id: int
    to_stash: bool
    quantity: int


class ItemCreate(BaseModel):
    item_name: str = "AR"
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 10
    category: ItemType = ItemType.Weapon


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
    weight: float = 0.0
    head_protection: int = 0
    chest_protection: int = 0
    stomach_protection: int = 0
    arm_protection: int = 0
    agility_penalty: float = -0.0


class FilterItemStats:
    class ClothingStats(Enum):
        CLOTHING_TYPE = "clothing_type"
        REPUTATION_BONUS = "reputation_bonus"
        MAX_ENERGY_BONUS = "max_energy_bonus"
        AGILITY_BONUS = "agility_bonus"
        HEALTH_BONUS = "health_bonus"
        LUCK_BONUS = "luck_bonus"
        STRENGTH_BONUS = "strength_bonus"
        KNOWLEDGE_BONUS = "knowledge_bonus"


    def list(self, item_class: Enum) -> List[str]:
        return [stat.value for stat in item_class]

    def get_relevant_stats(self, category: ItemType) -> List[str]:
        if category == ItemType.Clothing:
            return self.list(self.ClothingStats)
        return []

filter_item_stats = FilterItemStats()


openapi_item_examples = {
    "medical": {
        "summary": "Medical items",
        "value": {
            'item_name': 'Stimulant',
            'category': ItemType.Medical,
            'tier': ItemTier.Tier3,
            'quick_sell': 300,
            'health_increase': 20,
            'pain_reduction': 5,
            'weight_bonus': 10,
            'agility_bonus': 6,
            'amount_of_actions': 1
        },
    },
    "clothing": {
        "summary": "Clothing items",
        "description": "Types: 'Mask', 'Shirt', 'Legs'",
        "value": {
            'item_name': 'Cargo Pants',
            'category': ItemType.Clothing,
            'tier': ItemTier.Tier1,
            'quick_sell': 250,
            'clothing_type': ClothingType.Legs,
            'reputation_bonus': 0,
            'max_energy_bonus': 0,
            'agility_bonus': 0.0,
            'health_bonus': 0,
            'luck_bonus': 0.0,
            'strength_bonus': 0.0,
            'knowledge_bonus': 0.0
        },
    },
    "weapon": {
        "summary": "Weapons",
        "value": {
            'item_name': 'M4A1 Carbine',
            'category': ItemType.Weapon,
            'tier': ItemTier.Tier3,
            'quick_sell': 1500,
            'weight': 3.1,
            'caliber': '5.56x45mm NATO',
            'damage': 20,
            'strength': 0.0,
            'range': 300,
            'accuracy': 70,
            'reload_speed': 2.0,
            'fire_rate': 3.0,
            'magazine_size': 30,
            'armor_penetration': 20,
            'headshot_chance': 35,
            'agility_penalty': -2.0,
            'allowed_attachments': {
                "Muzzle": "Flash Suppressor",
                "Magazine": "Extended Magazine",
                "Scope": "Sniper Scope",
                "Stock": "Adjustable Stock",
                "Laser": "Tactical Laser"
            },
            'attachments': {},
        },
    },
    "bullet": {
        "summary": "Bullets",
        "value": {
            'item_name': '9x19mm',
            'category': ItemType.Bullets,
            'tier': ItemTier.Tier1,
            'quick_sell': 1,
            'armor_pen_adj': 0,
            'accuracy_adj': 0,
            'range_adj': 0,
            'damage_adj': 0,
            'fire_rate_adj': 0.0,
            'reload_speed_adj': 0.0
        },
    },
    "attachment": {
        "summary": "Attachments",
        "description": "Types: 'front_grip', 'muzzle', 'magazine', 'stock', 'scope', 'laser', 'flashlight', 'bipod', 'barrel',",
        "value": {
            'item_name': 'Polymer Rifle Bipod',
            'category': ItemType.Attachments,
            'tier': ItemTier.Tier4,
            'quick_sell': 800,
            'type': "front_grip",
            'weight_adj': 0.0,
            'damage_adj': 0,
            'range_adj': 0,
            'accuracy_adj': 0,
            'reload_speed_adj': 0.0,
            'fire_rate_adj': 0.0,
            'magazine_size_adj': 0,
            'headshot_chance_adj': 0,
            'agility_penalty_adj': 0.0
        },
    },
    "armor": {
        "summary": "Armor pieces",
        "description": "Types: 'Head', 'Body'",
        "value": {
            'item_name': 'Tactical Vest',
            'category': ItemType.Armor,
            'tier': ItemTier.Tier2,
            'quick_sell': 1500,
            'type': ArmorType.Body,
            'weight': 4.0,
            'head_protection': 0,
            'chest_protection': 30,
            'stomach_protection': 20,
            'arm_protection': 10,
            'agility_penalty': -0.3
        }
    }
}

