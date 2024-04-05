from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Stats(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    level: int
    health: int
    stamina: int
    strength: int
    intelligence: int
    knowledge: int
    user: Optional["User"] = Relationship(back_populates="stats")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(index=True) # Will be encrypted, but not for development purposes
    email: str = Field(index=True)
    stats_id: Optional[int] = Field(default=None, foreign_key="stats.id")
    stats: Optional[Stats] = Relationship(back_populates="user")