from typing import Optional, Dict
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

from .item_schema import ItemBase


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


class AttachmentRequest(BaseModel):
    weapon_inventory_id: int


class AddAttachmentsRequest(AttachmentRequest):
    attachments_to_add: Dict[AttachmentTypes, str] = {
        "Muzzle": "Flash Suppressor",
        "Stock": "Adjustable Stock",
        "Scope": "Sniper Scope",
        "Laser": "Tactical Laser"
    }


class RemoveAttachmentRequest(AttachmentRequest):
    attachments_to_remove: Dict[AttachmentTypes, str] = {
        "Laser": "Tactical Laser"
    }


class WeaponBase(SQLModel):
    damage: int = Field(default=0, nullable=False)
    strength_adj: float = Field(default=0)
    caliber: Optional[str]
    range: int = Field(default=0)  # In meters
    accuracy: int = Field(default=0)  # 80/100
    reload_speed: float = Field(default=0.0)  # In seconds
    fire_rate: float = Field(default=0.00)  # for Round-Per-Second
    magazine_size: int = Field(default=0)
    armor_penetration: int = Field(default=0)
    headshot_chance: int = Field(default=0)
    agility_adj: float = Field(default=-0.00)


class BulletBase(SQLModel):
    armor_pen_adj: int = Field(default=0)
    accuracy_adj: int = Field(default=0)
    range_adj: int = Field(default=0)
    damage_adj: int = Field(default=0)
    fire_rate_adj: float = Field(default=0.0)
    reload_speed_adj: float = Field(default=0.0)


class AttachmentBase(SQLModel):
    type: AttachmentTypes = Field(default=AttachmentTypes.Scope, nullable=False)
    damage_adj: int = Field(default=0)
    range_adj: int = Field(default=0)
    accuracy_adj: int = Field(default=0)
    reload_speed_adj: float = Field(default=0.0)
    fire_rate_adj: float = Field(default=0.0)
    magazine_size_adj: int = Field(default=0)
    headshot_chance_adj: int = Field(default=0)
    agility_adj: float = Field(default=0.00)


