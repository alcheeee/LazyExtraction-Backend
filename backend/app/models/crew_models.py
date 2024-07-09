from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Enum, Column, String
from .models import InventoryItem, User
from ..schemas import ItemTier


class CrewItems(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str
    tier: ItemTier = Field(sa_column=Column(Enum(ItemTier)), default=ItemTier.Tier1)
    quantity: int = Field(default=0)
    crew_id: Optional[int] = Field(default=None, foreign_key="crew.id")
    crew: Optional["Crew"] = Relationship(back_populates="items")


class Crew(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    leader: str
    private: bool = Field(default=False)
    capital: int = Field(default=0)
    reputation: int = Field(default=0)

    box_timer: int = Field(default=1440) # 24 hours in minutes, not added, just an idea
    better_box: int = Field(default=0)

    max_players: int = Field(default=0)

    current_activity: Optional[str] = Field(default=None)
    activity_progress: Optional[int] = Field(default=None)

    items: List[CrewItems] = Relationship(back_populates="crew")
    employees: List["User"] = Relationship(back_populates="crew")


