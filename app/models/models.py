import enum

from sqlmodel import SQLModel, Field, Enum, Relationship, Column, String
from typing import List, Optional


"""
Migrate Database:
python -m alembic revision --autogenerate -m "Added Items and sub-Tables"

change 'server_default' in migration version.py

python -m alembic upgrade head
"""


class Stats(SQLModel, table=True):
    """
    Stats Table for Users, linked by id
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    level: float
    reputation: int
    education: str
    max_energy: int
    evasiveness: int
    health: int
    strength: int
    knowledge: int
    user: Optional["User"] = Relationship(back_populates="stats")


class Inventory(SQLModel, table=True):
    """
    Inventory Table for Users, linked by id
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    cash: int
    bank: int
    energy: int
    user: Optional["User"] = Relationship(back_populates="inventory")


class Corporations(SQLModel, table=True):
    """
    Corporations Table | One-to-many
    id: Unique Corporation Identifier
    corp_type: [Crime, Industrial, Criminal Justice, ..?]
    employees: [user_id list]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    corporation_name: str
    corporation_type: str
    leader: int
    capital: Optional[int] = Field(default=0, nullable=False)
    reputation: Optional[int] = Field(default=0, nullable=False)
    employees: List["User"] = Relationship(back_populates="corporation")


class User(SQLModel, table=True):
    """
    User Table
    id: Unique User Identifier in database
    username: set by user
    password: set by user
    email: set by user
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    is_admin: bool = Field(default=False)
    username: str = Field(index=True)
    password: str = Field(index=True) # Will be encrypted, but not for development purposes
    email: str = Field(index=True)
    job: Optional[str] = Field(default=None)
    corp_id: Optional[int] = Field(default=None, foreign_key="corporations.id")
    corporation: Optional["Corporations"] = Relationship(back_populates="employees")
    stats_id: Optional[int] = Field(default=None, foreign_key="stats.id")
    stats: Optional[Stats] = Relationship(back_populates="user")
    inv_id: Optional[int] = Field(default=None, foreign_key="inventory.id")
    inventory: Optional[Inventory] = Relationship(back_populates="user")


class Jobs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    job_name: str
    job_type: str
    income: int
    energy_required: int
    description: str
    required_stats: str  # Json
    stat_changes: str


class ItemType(enum.Enum):
    Food = "Food"
    IndustrialCrafting = "IndustrialCrafting"
    Drug = "Drug"
    Weapon = "Weapon"
    Clothing = "Clothing"
    Other = "Other"


class Items(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str
    buy_price: Optional[int] = None
    quality: str
    illegal: bool
    category: ItemType = Field(sa_column=Column(Enum(ItemType)))


    # Relationships
    food_items: Optional["FoodItems"] = Relationship(back_populates="item", sa_relationship_kwargs={"uselist": False})
    weapon_details: Optional["Weapon"] = Relationship(back_populates="item", sa_relationship_kwargs={"uselist": False})
    industrial_crafting_details: Optional["IndustrialCrafting"] = Relationship(back_populates="item", sa_relationship_kwargs={"uselist": False})
    black_market_posts: Optional["BlackMarket"] = Relationship(back_populates="item")


class FoodItems(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    health_bonus: int
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


class IndustrialCrafting(SQLModel, table=True):
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


class BlackMarket(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    who_posted: str
    item_id: int = Field(default=None, foreign_key="items.id")
    time_posted: str
    sell_price: int

    item: Optional[Items] = Relationship(back_populates="black_market_posts")




