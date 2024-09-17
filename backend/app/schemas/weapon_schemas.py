from typing import Optional, Dict
from enum import Enum
from .item_schema import ItemCreate
from pydantic import BaseModel


class AttachmentTypes(str, Enum):
    FrontGrip = "FrontGrip"
    Muzzle = "Muzzle"
    Magazine = "Magazine"
    Stock = "Stock"
    Scope = "Scope"
    Laser = "Laser"
    Flashlight = "Flashlight"
    Bipod = "Bipod"
    Barrel = "Barrel"


class AddAttachmentsRequest(BaseModel):
    weapon_inventory_id: int
    attachments_to_add: Dict[AttachmentTypes, str] = {
        "Muzzle": "Flash Suppressor",
        "Stock": "Adjustable Stock",
        "Scope": "Sniper Scope",
        "Laser": "Tactical Laser"
    }


class WeaponCreate(ItemCreate):
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
    damage_adj: int = 0
    range_adj: int = 0
    accuracy_adj: int = 0
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 0
    agility_penalty_adj: float = 0.0


