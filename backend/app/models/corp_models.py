from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Enum, Column
from .models import InventoryItem, User
from ..schemas.corporation_schema import CorporationType


class CorpInventoryItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_name: str
    quality: str = Field(default="Junk")
    quantity: int = Field(default=0)
    corp_inventory_id: Optional[int] = Field(default=None, foreign_key="corpinventory.id")
    corp_inventory: Optional["CorpInventory"] = Relationship(back_populates="items")

class CorpInventory(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    corporation_id: Optional[int] = Field(default=None, foreign_key="corporation.id")
    items: List[CorpInventoryItem] = Relationship(back_populates="corp_inventory")
    corporation: Optional["Corporation"] = Relationship(back_populates="corp_inventory")

class CorpUpgrades(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    corporation_id: Optional[int] = Field(default=None, foreign_key="corporation.id")
    corporation: "Corporation" = Relationship(back_populates="corp_upgrades")
    industrial_production: int = Field(default=0, title="Production Efficiency")
    industrial_level: int = Field(default=0, title="Industrial Level")
    criminal_networks: int = Field(default=0, title="Criminal Network Connections")
    criminal_money_laundering: int = Field(default=0, title="Money Laundering Capability")
    law_forensics: int = Field(default=0, title="Forensics Capability")
    law_legal_frameworks: int = Field(default=0, title="Legal Efficiency")

class CorpActivities(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    cost: int = Field(default=None)
    reward: str = Field(default=None)
    preperation: int = Field(default=0)
    progress: int = Field(default=0)
    progress_required: int = Field(default=100)
    required_rep: int = Field(default=0)
    corporation_id: Optional[int] = Field(default=None, foreign_key="corporation.id")
    corporation: Optional["Corporation"] = Relationship(back_populates="corp_activities")

class Corporation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    corporation_name: str
    corporation_type: CorporationType = Field(sa_column=Enum(CorporationType))
    leader: str
    private: bool = Field(default=False)
    capital: int = Field(default=0)
    reputation: int = Field(default=0)
    employees: List["User"] = Relationship(back_populates="corporation")
    corp_inventory: Optional[CorpInventory] = Relationship(back_populates="corporation")
    corp_upgrades: Optional[CorpUpgrades] = Relationship(back_populates="corporation")
    corp_activities: List[CorpActivities] = Relationship(back_populates="corporation")


