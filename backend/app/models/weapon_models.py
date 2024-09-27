from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, Enum
from sqlalchemy.dialects.postgresql import JSONB
from app.schemas import AttachmentTypes
from . import Items
from app.schemas.weapon_schemas import (
    BulletBase,
    WeaponBase,
    AttachmentBase
)


class Bullets(BulletBase, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="bullet_details")


class Attachments(AttachmentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="attachment_details")


class Weapon(WeaponBase, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="weapon_details")
