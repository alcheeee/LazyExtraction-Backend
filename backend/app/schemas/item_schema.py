from enum import Enum
from typing import Optional, List, Any
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Relationship
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


class StashStatusSwitchRequest(BaseModel):
    inventory_item_id: int
    to_stash: bool
    quantity: int


class EquippingUnequippingRequest(BaseModel):
    inventory_item_id: int


class ItemBase(SQLModel):
    item_name: str = Field(index=True)
    category: ItemType = Field(default=ItemType.Weapon, nullable=False)
    tier: ItemTier = Field(default=ItemTier.Tier1, nullable=False)
    quick_sell: int = Field(default=5)
    weight: float = Field(default=0.0)
    can_be_modified: bool = Field(default=False, nullable=False)
    allowed_modifications: Optional[dict[str, Any]] = Field(default=None, sa_type=JSONB)


class MedicalBase(SQLModel):
    health_adj: int = Field(default=0)
    pain_reduction: int = Field(default=0)
    agility_adj: int = Field(default=0)


class ClothingBase(SQLModel):
    clothing_type: ClothingType = Field(default=ClothingType.Mask, nullable=False)
    reputation_adj: int = Field(default=0)
    max_energy_adj: int = Field(default=0)
    agility_adj: float = Field(default=0)
    health_adj: int = Field(default=0)
    strength_adj: float = Field(default=0)
    knowledge_adj: float = Field(default=0)
    luck_adj: float = Field(default=0)


class ArmorBase(SQLModel):
    type: ArmorType = Field(default=ArmorType.Body, nullable=False)
    head_protection_adj: int = Field(default=0)
    chest_protection_adj: int = Field(default=0)
    stomach_protection_adj: int = Field(default=0)
    arm_protection_adj: int = Field(default=0)
    agility_adj: float = Field(default=0.00)
