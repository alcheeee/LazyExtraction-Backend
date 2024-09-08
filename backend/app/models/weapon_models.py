from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column, Enum
from sqlalchemy.dialects.postgresql import JSON
from ..schemas import AttachmentTypes
from . import Items


class Bullets(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    armor_pen_adj: int = Field(default=0)
    accuracy_adj: int = Field(default=0)
    range_adj: int = Field(default=0)
    damage_adj: int = Field(default=0)
    fire_rate_adj: float = Field(default=0.0)
    reload_speed_adj: float = Field(default=0.0)

    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional[Items] = Relationship(back_populates="bullet_details")


class Attachments(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    type: AttachmentTypes = Field(sa_column=Column(Enum(AttachmentTypes)))
    weight_adj: float = Field(default=0.0)
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


class Weapon(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    damage: int = Field(default=0, nullable=False)
    strength: float = Field(default=0)

    weight: float = Field(default=5.0)  # in pounds

    # For Guns only
    attachments: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    allowed_attachments: Optional[dict] = Field(default=None, sa_column=Column(JSON))

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

    def apply_attachment_stats(self, attachment_data):
        self.damage += attachment_data.get('damage_adj', 0)
        self.strength += attachment_data.get('strength_adj', 0.0)
        self.weight += attachment_data.get('weight_adj', 0.0)
        self.range += attachment_data.get('range_adj', 0)
        self.accuracy += attachment_data.get('accuracy_adj', 0)
        self.reload_speed += attachment_data.get('reload_speed_adj', 0.0)
        self.fire_rate += attachment_data.get('fire_rate_adj', 0.0)
        self.magazine_size += attachment_data.get('magazine_size_adj', 0)
        self.armor_penetration += attachment_data.get('armor_pen_adj', 0)
        self.headshot_chance += attachment_data.get('headshot_chance_adj', 0)
        self.agility_penalty += attachment_data.get('agility_penalty_adj', 0.0)

    def remove_attachment_stats(self, attachment_data):
        self.damage -= attachment_data.get('damage_adj', 0)
        self.strength -= attachment_data.get('strength_adj', 0.0)
        self.weight -= attachment_data.get('weight_adj', 0.0)
        self.range -= attachment_data.get('range_adj', 0)
        self.accuracy -= attachment_data.get('accuracy_adj', 0)
        self.reload_speed -= attachment_data.get('reload_speed_adj', 0.0)
        self.fire_rate -= attachment_data.get('fire_rate_adj', 0.0)
        self.magazine_size -= attachment_data.get('magazine_size_adj', 0)
        self.armor_penetration -= attachment_data.get('armor_pen_adj', 0)
        self.headshot_chance -= attachment_data.get('headshot_chance_adj', 0)
        self.agility_penalty -= attachment_data.get('agility_penalty_adj', 0.0)