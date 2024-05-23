from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column, Enum
from ..schemas import AttachmentTypes
from . import Items


class Weapon(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    damage_bonus: int = Field(default=0, nullable=False)
    strength_bonus: float = Field(default=0)

    weight: float = Field(default=5.0)  # in pounds
    max_durability: int = Field(default=100)
    current_durability: float = Field(default=100.00)

    # For Guns only
    attachments: Optional[str] = Field(default=None)
    allowed_attachments: Optional[str] = Field(default=None)

    caliber: Optional[str]
    range: int = Field(default=0)  # In meters
    accuracy: int = Field(default=0)  # 80/100
    reload_speed: float = Field(default=0.0)  # In seconds
    fire_rate: float = Field(default=0.00)  # for Round-Per-Second

    # Bullet/Attachment related
    magazine_size: int = Field(default=0)
    armor_penetration: int = Field(default=0)
    headshot_chance: int = Field(default=0)
    agility_penalty: float = Field(default=-0.00)

    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="weapon_details")


class Bullets(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    armor_pen_bonus: int = Field(default=0)
    accuracy_bonus: int = Field(default=0)
    range_bonus: int = Field(default=0)

    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="bullet_details")


class Attachments(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    type: AttachmentTypes = Field(sa_column=Column(Enum(AttachmentTypes)))
    weight_adj: float = Field(default=0.0)
    max_durability_adj: int = Field(default=0)
    damage_adj: int = Field(default=0)
    range_adj: int = Field(default=0)
    accuracy_adj: int = Field(default=0)
    reload_speed_adj: float = Field(default=0.0)
    fire_rate_adj: float = Field(default=0.0)
    magazine_size_adj: int = Field(default=0)
    headshot_chance_adj: int = Field(default=0)
    agility_penalty_adj: float = Field(default=0.00)

    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="attachment_details")
