from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Stats(SQLModel, table=True):
    """
    Stats Table for Users, linked by id
    id: Unique User Identifier in database
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    cash: int
    bank: int
    education: str
    level: int
    energy: int
    health: int
    stamina: int
    strength: int
    intelligence: int
    knowledge: int
    user: Optional["User"] = Relationship(back_populates="stats")


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
    employees: List["User"] = Relationship(back_populates="corporation")


