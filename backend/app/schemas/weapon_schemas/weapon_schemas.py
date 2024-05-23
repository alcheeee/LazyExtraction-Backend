from typing import Optional, Dict
from enum import Enum
from ..item_schema import ItemCreate


weapon_bonus_wrapper = {
    "strength": "strength",
    "damage": "damage",
    "agility": "agility_penalty"
}


class AttachmentTypes(str, Enum):
    FrontGrip = "front_grip"
    Muzzle = "muzzle"
    Magazine = "magazine"
    Stock = "stock"
    Scope = "scope"
    Laser = "laser"
    Flashlight = "flashlight"
    Bipod = "bipod"
    Barrel = "barrel"


class WeaponCreate(ItemCreate):
    allowed_attachments: Optional[Dict[str, str]] = {}
    attachments: Optional[Dict[str, str]] = {}

    weight: float = 3.5
    max_durability: int = 100
    current_durability: float = 100.0
    caliber: Optional[str]
    damage: int = 0
    strength: float = 0.0
    range: int = 5
    accuracy: int = 50
    reload_speed: float = 0
    fire_rate: float = 0
    magazine_size: int = 0
    armor_penetration: int = 0
    headshot_chance: int = 0
    agility_penalty: float = -1.4


class BulletCreate(ItemCreate):
    armor_pen_adj: int = 0
    accuracy_adj: int = 0
    range_adj: int = 0
    damage_adj: int = 0
    fire_rate_adj: float = 0.0
    reload_speed_adj: float = 0.0


class AttachmentCreate(ItemCreate):
    type: AttachmentTypes = AttachmentTypes.Bipod
    weight_adj: float = 0.0
    max_durability_adj: int = 0
    damage_adj: int = 0
    range_adj: int = 0
    accuracy_adj: int = 0
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 0
    agility_penalty_adj: float = 0.0


