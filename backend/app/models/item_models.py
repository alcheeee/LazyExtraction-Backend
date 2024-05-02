from typing import Optional, List
from sqlalchemy import Enum, Column, Integer
from sqlmodel import SQLModel, Field, Relationship
from ..schemas.item_schema import ItemType, ItemQuality


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
    black_market_posts: Optional["BlackMarket"] = Relationship(back_populates="item")
    general_market_items: Optional["GeneralMarket"] = Relationship(back_populates="item")


class Weapon(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    damage_bonus: int
    evasiveness_bonus: int = Field(default=None, nullable=True)
    strength_bonus: int = Field(default=None, nullable=True)
    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="weapon_details")


class Clothing(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    clothing_type: str
    reputation_bonus: Optional[int] = Field(default=None, nullable=True)
    max_energy_bonus: Optional[int] = Field(default=None, nullable=True)
    evasiveness_bonus: Optional[float] = Field(default=None, nullable=True)
    health_bonus: Optional[int] = Field(default=None, nullable=True)
    luck_bonus: Optional[float] = Field(default=None, nullable=True)
    strength_bonus: Optional[float] = Field(default=None, nullable=True)
    knowledge_bonus: Optional[float] = Field(default=None, nullable=True)
    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="clothing_details")


class GeneralMarket(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_cost: int = Field(default=0)
    sell_price: int = Field(default=0)
    item_quantity: int
    item_quality: str
    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="general_market_items")


class BlackMarket(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    sell_price: int = Field(default=0)
    item_quantity: int
    item_quality: str
    by_user: str
    time_posted: str
    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="black_market_posts")
