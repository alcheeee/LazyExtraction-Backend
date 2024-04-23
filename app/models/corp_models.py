from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.models import InventoryItem, User


class CorpInventoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_name: str
    quality: str = Field(default="Junk")
    quantity: int = Field(default=0)
    corp_inventory_id: Optional[int] = Field(default=None, foreign_key="corpinventory.id")
    corp_inventory: Optional["CorpInventory"] = Relationship(back_populates="items")

class CorpInventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    corporation_id: Optional[int] = Field(default=None, foreign_key="corporations.id")
    items: List[CorpInventoryItem] = Relationship(back_populates="corp_inventory")
    corporation: Optional["Corporations"] = Relationship(back_populates="corp_inventory")


class Corporations(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    corporation_name: str
    corporation_type: str
    leader: str
    private: bool = Field(default=False)
    capital: int = Field(default=0)
    reputation: int = Field(default=0)
    employees: List["User"] = Relationship(back_populates="corporation")
    corp_inventory: Optional[CorpInventory] = Relationship(back_populates="corporation")
