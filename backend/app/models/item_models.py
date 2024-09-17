from datetime import datetime
from typing import Optional, List, Any
from sqlalchemy import Enum, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Relationship
from ..schemas import ItemType, ItemTier, ClothingType, ArmorType


item_relationship = Relationship(
    back_populates="item",
    sa_relationship_kwargs={"uselist": False}
)


class Items(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str = Field(index=True)
    category: ItemType = Field(default=ItemType.Weapon, nullable=False)
    tier: ItemTier = Field(default=ItemTier.Tier1, nullable=False)
    quick_sell: int = Field(default=5)
    weight: float = Field(default=0.0)

    can_be_modified: bool = Field(default=False, nullable=False)
    allowed_modifications: Optional[dict[str, Any]] = Field(default=None, sa_type=JSONB)

    # Relationships
    market_items: List["MarketItems"] = Relationship(back_populates="item")
    weapon_details: Optional["Weapon"] = item_relationship
    clothing_details: Optional["Clothing"] = item_relationship
    armor_details: Optional["Armor"] = item_relationship
    medical_details: Optional["Medical"] = item_relationship
    bullet_details: Optional["Bullets"] = item_relationship
    attachment_details: Optional["Attachments"] = item_relationship


class Medical(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    health_increase: int = Field(default=0)
    pain_reduction: int = Field(default=0)
    weight_bonus: int = Field(default=0)
    agility_bonus: int = Field(default=0)
    amount_of_actions: int = Field(default=0)

    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="medical_details")


class Armor(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    type: ArmorType = Field(default=ArmorType.Body, nullable=False)
    head_protection: int = Field(default=5)
    chest_protection: int = Field(default=5)
    stomach_protection: int = Field(default=5)
    arm_protection: int = Field(default=5)
    agility_penalty: float = Field(default=-0.01)

    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="armor_details")


class Clothing(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    clothing_type: ClothingType = Field(default=ClothingType.Mask, nullable=False)
    reputation_bonus: int = Field(default=0)
    max_energy_bonus: int = Field(default=0)
    agility_bonus: float = Field(default=0)
    health_bonus: int = Field(default=0)
    strength_bonus: float = Field(default=0)
    knowledge_bonus: float = Field(default=0)
    luck_bonus: float = Field(default=0)

    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="clothing_details")


class Market(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str = Field(index=True)
    postings: List["MarketItems"] = Relationship(back_populates="main_market_post")


class MarketItems(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str = Field(default="")
    item_cost: int = Field(default=0)
    quick_sell_value: int = Field(default=0),
    item_quantity: int = Field(default=0)
    by_user: Optional[str] = Field(default=None, nullable=True)
    posted_at: datetime = Field(default_factory=datetime.now)

    is_modified: bool = Field(default=False)
    modifications: Optional[dict[str, Any]] = Field(default={}, sa_type=JSONB)

    item_id: int = Field(default=None, foreign_key="items.id")
    main_market_post_id: int = Field(default=None, foreign_key="market.id")

    item: Optional[Items] = Relationship(back_populates="market_items")
    main_market_post: Optional[Market] = Relationship(back_populates="postings")
