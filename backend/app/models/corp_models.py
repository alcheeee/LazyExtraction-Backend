from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Enum, Column, String
from .models import InventoryItem, User
from ..schemas import CorporationType, ItemTier


class CorporationItems(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str
    tier: ItemTier = Field(sa_column=Column(Enum(ItemTier)), default=ItemTier.Tier1)
    quantity: int = Field(default=0)
    corporation_id: Optional[int] = Field(default=None, foreign_key="corporation.id")
    corporation: Optional["Corporation"] = Relationship(back_populates="items")

class Corporation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: CorporationType = Field(sa_column=Enum(CorporationType))
    name: str = Field(index=True, unique=True)
    leader: str
    private: bool = Field(default=False)
    capital: int = Field(default=0)
    reputation: int = Field(default=0)

    upgrade_one: int = Field(default=0)
    upgrade_two: int = Field(default=0)

    current_activity: Optional[str] = Field(default=None)
    activity_progress: Optional[int] = Field(default=None)
    activity_reward_id: Optional[int] = Field(default=None)

    items: List[CorporationItems] = Relationship(back_populates="corporation")
    employees: List["User"] = Relationship(back_populates="corporation")


