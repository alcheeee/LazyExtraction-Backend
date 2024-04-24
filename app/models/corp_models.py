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

class CorpUpgrades(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    industrial_production: Optional[int] # Increase Production Amount
    industrial_level: Optional[int]      # Unlocks better items to craft
    criminal_networks: Optional[int]          # Increase success rate of crime
    criminal_money_laundering: Optional[int]  # Increase chance to get away with capital
    law_forensics: Optional[int]        # Increases evidence gathering
    law_legal_frameworks: Optional[int] # Increase chance to win in legal battles
    corporation_id: Optional[int] = Field(default=None, foreign_key="corporations.id")
    corporation: Optional["Corporations"] = Relationship(back_populates="corp_upgrades")

class CorpActivities(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    cost: int = Field(default=None)
    reward: str = Field(default=None)
    preperation: int = Field(default=0)
    progress: int = Field(default=0)
    progress_required: int = Field(default=100)
    required_rep: int = Field(default=0)
    corporation_id: Optional[int] = Field(default=None, foreign_key="corporations.id")
    corporation: Optional["Corporations"] = Relationship(back_populates="corp_activities")

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
    corp_upgrades: Optional[CorpUpgrades] = Relationship(back_populates="corporation")
    corp_activities: Optional[CorpActivities] = Relationship(back_populates="corporation")


