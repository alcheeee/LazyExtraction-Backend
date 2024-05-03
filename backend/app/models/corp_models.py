from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Enum, Column
from .models import InventoryItem, User
from ..schemas.corporation_schema import CorporationType


class CorporationItems(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str
    quality: str = Field(default="Junk")
    quantity: int = Field(default=0)
    corporation_id: Optional[int] = Field(default=None, foreign_key="corporation.id")
    corporation: Optional["Corporation"] = Relationship(back_populates="items")

class Corporation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: CorporationType = Field(sa_column=Enum(CorporationType))
    name: str = Field(index=True)
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


