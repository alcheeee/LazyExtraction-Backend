from datetime import datetime
from typing import Optional, List, Any
from sqlalchemy import Enum, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Relationship
from app.schemas import ItemType, ItemTier, ClothingType, ArmorType
from app.schemas.item_schema import (
    ItemBase,
    ArmorBase,
    ClothingBase,
    MedicalBase
)

item_relationship = Relationship(
    back_populates="item",
    sa_relationship_kwargs={"uselist": False}
)


class Items(ItemBase, table=True):
    id: int = Field(default=None, primary_key=True)
    market_items: List["MarketItems"] = Relationship(back_populates="item")
    weapon_details: Optional["Weapon"] = item_relationship
    clothing_details: Optional["Clothing"] = item_relationship
    armor_details: Optional["Armor"] = item_relationship
    medical_details: Optional["Medical"] = item_relationship
    bullet_details: Optional["Bullets"] = item_relationship
    attachment_details: Optional["Attachments"] = item_relationship


class Medical(MedicalBase, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="medical_details")


class Armor(ArmorBase, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="armor_details")


class Clothing(ClothingBase, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="clothing_details")


class MarketItems(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str = Field(default="", index=True)
    item_cost: int = Field(default=0)
    quick_sell_value: int = Field(default=0),
    item_quantity: int = Field(default=0)
    by_user: Optional[str] = Field(default=None, nullable=True)
    posted_at: datetime = Field(default_factory=datetime.now)

    is_modified: bool = Field(default=False)
    modifications: Optional[dict[str, Any]] = Field(default={}, sa_type=JSONB)

    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="market_items")
