import enum
from typing import Optional
from sqlalchemy import Enum, Column
from sqlmodel import SQLModel, Field, Relationship


class ItemType(enum.Enum):
    Food = "Food"
    IndustrialCrafting = "IndustrialCrafting"
    Drug = "Drug"
    Weapon = "Weapon"
    Clothing = "Clothing"
    Other = "Other"


class ItemQuality(enum.Enum):
    Junk = 'Junk'
    Common = 'Common'
    Uncommon = 'Uncommon'
    Rare = 'Rare'
    Special = 'Special'
    Unique = 'Unique'


class Items(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str
    buy_price: Optional[int] = None
    quality: ItemQuality = Field(sa_column=Column(Enum(ItemQuality)))
    illegal: bool
    category: ItemType = Field(sa_column=Column(Enum(ItemType)))
    # Relationships
    food_items: Optional["FoodItems"] = Relationship(back_populates="item", sa_relationship_kwargs={"uselist": False})
    weapon_details: Optional["Weapon"] = Relationship(back_populates="item", sa_relationship_kwargs={"uselist": False})
    industrial_crafting_details: Optional["IndustrialCraftingRecipes"] = Relationship(back_populates="item", sa_relationship_kwargs={"uselist": False})
    black_market_posts: Optional["BlackMarket"] = Relationship(back_populates="item")
    general_market_items: Optional["GeneralMarket"] = Relationship(back_populates="item")


class FoodItems(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    health_increase: int
    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="food_items")


class Weapon(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    damage: int
    damage_bonus: Optional[int] = None
    evasiveness_bonus: Optional[int] = None
    strength_bonus: Optional[int] = None
    attachment_one: Optional[str] = None
    attachment_two: Optional[str] = None
    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="weapon_details")


class IndustrialCraftingRecipes(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_one: str
    item_one_amount: int
    item_two: str
    item_two_amount: int
    item_three: str
    item_three_amount: int
    item_produced: str
    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="industrial_crafting_details")




class GeneralMarket(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str
    item_cost: int
    item_sell: int
    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="general_market_items")


class BlackMarket(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    who_posted: str
    time_posted: str
    sell_price: int
    item_id: int = Field(default=None, foreign_key="items.id")
    item: Optional[Items] = Relationship(back_populates="black_market_posts")
