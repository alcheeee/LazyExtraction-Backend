from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

"""
Migrate Database:

python -m alembic revision --autogenerate -m "Corporation Capital & Rep"

change 'server_default' in migration version.py

python -m alembic upgrade head
"""


class Stats(SQLModel, table=True):
    """
    Stats Table for Users, linked by id
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    level: int
    reputation: int
    education: str
    max_energy: int
    health: int
    stamina: int
    strength: int
    intelligence: int
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