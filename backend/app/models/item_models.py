from datetime import datetime
from typing import Optional, List
from sqlalchemy import Enum, Column, Integer
from sqlmodel import SQLModel, Field, Relationship
from ..schemas.item_schema import ItemType, ItemQuality, ClothingType
from ..schemas.market_schema import MarketNames


class Items(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str
    category: ItemType = Field(sa_column=Column(Enum(ItemType)))
    quality: ItemQuality = Field(sa_column=Column(Enum(ItemQuality)))
    illegal: bool = Field(default=False)
    quantity: int = Field(default=0)

    # Relationships
    weapon_details: Optional["Weapon"] = Relationship(back_populates="item", sa_relationship_kwargs={"uselist": False})
    clothing_details: Optional["Clothing"] = Relationship(back_populates="item", sa_relationship_kwargs={"uselist": False})
    market_items: Optional["MarketItems"] = Relationship(back_populates="item")


class Weapon(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    damage_bonus: int = Field(default=0, nullable=False)
    evasiveness_bonus: float = Field(default=0)
    strength_bonus: float = Field(default=0)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="weapon_details")


class Clothing(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    clothing_type: ClothingType = Field(default=ClothingType.Mask, nullable=False)
    reputation_bonus: int = Field(default=0)
    max_energy_bonus: int = Field(default=0)
    evasiveness_bonus: float = Field(default=0)
    health_bonus: int = Field(default=0)
    strength_bonus: float = Field(default=0)
    knowledge_bonus: float = Field(default=0)
    luck_bonus: float = Field(default=0)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="clothing_details")


class MarketItems(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    market_name: MarketNames = Field(default=MarketNames.GeneralMarket, nullable=False, index=True)
    item_cost: int = Field(default=0)
    item_quantity: int
    can_be_illegal: bool = Field(default=False)
    sell_price: int = Field(default=0, nullable=True)
    by_user: str = Field(default=None, nullable=True)
    posted_at: datetime = Field(default_factory=datetime.utcnow)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="market_items")
