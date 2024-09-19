from sqlmodel import SQLModel, Field, Relationship, Column, Enum
from sqlalchemy.dialects.postgresql import JSONB
from typing import List, Optional, Any
from datetime import datetime
from ..schemas.world_schemas import WorldNames


class Stats(SQLModel, table=True):
    """
    Stats Table for Users, linked by id
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    level: float = Field(default=1.00)
    reputation: float = Field(default=1.00)
    max_energy: int = Field(default=100)
    luck: float = Field(default=1.00)
    knowledge: float = Field(default=1.00)
    max_weight: float = Field(default=100.00)  # in pounds

    # Combat related
    agility: float = Field(default=1.00)
    health: int = Field(default=100)
    damage: int = Field(default=0)
    strength: float = Field(default=1.00)

    head_protection: int = Field(default=1)
    chest_protection: int = Field(default=1)
    stomach_protection: int = Field(default=1)
    arm_protection: int = Field(default=1)

    user: Optional["User"] = Relationship(back_populates="stats")

    async def round_stats(self):
        float_attributes = ['level', 'reputation', 'agility', 'strength', 'knowledge', 'luck', 'max_weight']
        for attr in float_attributes:
            value = getattr(self, attr)
            if isinstance(value, float):
                setattr(self, attr, round(value, 2))


class TrainingProgress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Allow to go over 100, for every 100, thats a new "Level" of training
    basic_training: float = Field(default=0.00)
    advanced_infantry: float = Field(default=0.00)
    special_operations: float = Field(default=0.00)
    intelligence: float = Field(default=0.00)
    engineering: float = Field(default=0.00)
    medical: float = Field(default=0.00)
    leadership: float = Field(default=0.00)
    economics: float = Field(default=0.00)

    user: Optional["User"] = Relationship(back_populates="training_progress")


class Inventory(SQLModel, table=True):
    """Inventory Table for Users, linked by id"""
    id: Optional[int] = Field(default=None, primary_key=True)
    bank: int = Field(default=1000)
    energy: int = Field(default=100)
    current_weight: float = Field(default=0.0)
    equipped_weapon_id: Optional[int] = Field(default=None)
    equipped_mask_id: Optional[int] = Field(default=None)
    equipped_body_id: Optional[int] = Field(default=None)
    equipped_legs_id: Optional[int] = Field(default=None)
    equipped_body_armor_id: Optional[int] = Field(default=None)
    equipped_head_armor_id: Optional[int] = Field(default=None)

    items: List["InventoryItem"] = Relationship(back_populates="inventory")
    user: Optional["User"] = Relationship(back_populates="inventory")


class InventoryItem(SQLModel, table=True):
    """Represents individual items within a user's inventory"""
    id: int = Field(default=None, primary_key=True)
    item_name: str = Field(default="", nullable=False)
    amount_in_stash: int = Field(default=0)
    amount_in_inventory: int = Field(default=0)
    one_equipped: bool = Field(default=False)
    inventory_id: int = Field(default=None, foreign_key="inventory.id", index=True)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    is_modified: bool = Field(default=False, nullable=False)
    quick_sell_value: int = Field(default=0, nullable=False)
    modifications: Optional[dict[str, Any]] = Field(default={}, sa_type=JSONB)

    inventory: Optional["Inventory"] = Relationship(back_populates="items")
    item: Optional["Items"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


class User(SQLModel, table=True):
    """User Table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    is_admin: bool = Field(default=False)
    username: str = Field(index=True, unique=True)
    password: str
    email: Optional[str] = Field(index=True, unique=True)
    guest_account: Optional[bool] = Field(default=True)
    job: Optional[str] = Field(default=None)
    training: Optional[str] = Field(default=None)

    # "Raid" information
    in_raid: bool = Field(default=False, nullable=False)
    actions_left: Optional[int] = Field(default=None)
    current_world: Optional[WorldNames] = Field(default=None, sa_column=Column(Enum(WorldNames)))
    current_room_data: dict = Field(default=None, sa_type=JSONB)

    #FKeys
    training_progress_id: Optional[int] = Field(default=None, foreign_key="trainingprogress.id", index=True)
    inventory_id: Optional[int] = Field(default=None, foreign_key="inventory.id", index=True)
    stats_id: Optional[int] = Field(default=None, foreign_key="stats.id", index=True)
    crew_id: Optional[int] = Field(default=None, foreign_key="crew.id", index=True)

    # Relationships
    training_progress: Optional["TrainingProgress"] = Relationship(back_populates="user")
    stats: Optional["Stats"] = Relationship(back_populates="user")
    inventory: Optional["Inventory"] = Relationship(back_populates="user")
    crew: Optional["Crew"] = Relationship(back_populates="employees")
