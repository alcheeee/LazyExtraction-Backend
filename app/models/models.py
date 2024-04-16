from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Stats(SQLModel, table=True):
    """
    Stats Table for Users, linked by id
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    level: float
    reputation: int
    education: str
    max_energy: int
    damage: int
    evasiveness: float
    health: int
    luck: float
    strength: float
    knowledge: float
    user: Optional["User"] = Relationship(back_populates="stats")
    def round_stats(self):
        float_attributes = ['level', 'evasiveness', 'strength', 'knowledge', 'luck']
        for attr in float_attributes:
            value = getattr(self, attr)
            if isinstance(value, float):
                setattr(self, attr, round(value, 2))


class Inventory(SQLModel, table=True):
    """
    Inventory Table for Users, linked by id
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    bank: int
    energy: int
    inventory_items: str
    equipped_weapon: Optional[int] = Field(default=None, foreign_key="items.id", nullable=True)
    equipped_body: Optional[int] = Field(default=None, foreign_key="items.id", nullable=True)
    equipped_legs: Optional[int] = Field(default=None, foreign_key="items.id", nullable=True)
    equipped_mask: Optional[int] = Field(default=None, foreign_key="items.id", nullable=True)
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
    leader: str
    capital: Optional[int] = Field(default=0, nullable=False)
    reputation: Optional[int] = Field(default=0, nullable=False)
    corp_inventory: str
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
    password: str = Field(index=True)
    email: str = Field(index=True)
    job: Optional[str] = Field(default=None)
    corp_id: Optional[int] = Field(default=None, foreign_key="corporations.id")
    corporation: Optional["Corporations"] = Relationship(back_populates="employees")
    stats_id: Optional[int] = Field(default=None, foreign_key="stats.id")
    stats: Optional[Stats] = Relationship(back_populates="user")
    inv_id: Optional[int] = Field(default=None, foreign_key="inventory.id")
    inventory: Optional[Inventory] = Relationship(back_populates="user")




