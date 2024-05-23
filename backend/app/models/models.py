from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


class Stats(SQLModel, table=True):
    """
    Stats Table for Users, linked by id
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    level: float = Field(default=1.00)
    reputation: float = Field(default=1.00)
    max_energy: int = Field(default=100)
    luck: float = Field(default=1.00)
    knowledge: float = Field(default=1.00)
    max_weight: float = Field(default=100.00)  # in pounds

    # Combat related
    agility: float = Field(default=1.00)
    health: int = Field(default=100)
    damage: int = Field(default=1)
    strength: float = Field(default=1.00)

    head_protection: int = Field(default=5)
    chest_protection: int = Field(default=5)
    stomach_protection: int = Field(default=5)
    arm_protection: int = Field(default=5)

    user: Optional["User"] = Relationship(back_populates="stats")
    def round_stats(self):
        float_attributes = ['level', 'reputation', 'agility', 'strength', 'knowledge', 'luck', 'max_weight']
        for attr in float_attributes:
            value = getattr(self, attr)
            if isinstance(value, float):
                setattr(self, attr, round(value, 2))


class TrainingProgress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Allow to go over 100, for every 100, thats a new "Level" of training
    basic_training: float = Field(default=0.00)
    advanced_infantry: float = Field(default=0.00)
    special_operations: float = Field(default=0.00)
    intelligence: float = Field(default=0.00)
    engineering: float = Field(default=0.00)
    medical: float = Field(default=0.00)
    leadership: float = Field(default=0.00)
    economics: float = Field(default=0.00)

    user: Optional["User"] = Relationship(back_populates="training_progress")


class Inventory(SQLModel, table=True):
    """
    Inventory Table for Users, linked by id
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    bank: int = Field(default=1000)
    energy: int = Field(default=100)
    equipped_weapon_id: Optional[int] = Field(default=None)
    equipped_mask_id: Optional[int] = Field(default=None)
    equipped_body_id: Optional[int] = Field(default=None)
    equipped_legs_id: Optional[int] = Field(default=None)
    equipped_body_armor_id: Optional[int] = Field(default=None)
    equipped_head_armor_id: Optional[int] = Field(default=None)
    items: List["InventoryItem"] = Relationship(back_populates="inventory")
    user: Optional["User"] = Relationship(back_populates="inventory")


class InventoryItem(SQLModel, table=True):
    """
    Represents individual items within a user's inventory.
    """
    id: int = Field(default=None, primary_key=True)
    quantity: int = Field(default=0)
    inventory_id: int = Field(default=None, foreign_key="inventory.id", index=True)
    inventory: Optional["Inventory"] = Relationship(back_populates="items")
    item_id: int = Field(default=None, foreign_key="items.id", index=True)
    item: Optional["Items"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


class FriendsLink(SQLModel, table=True):
    user1_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    user2_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)


class User(SQLModel, table=True):
    """User Table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    is_admin: bool = Field(default=False)
    username: str = Field(index=True, unique=True)
    password: str
    email: str = Field(index=True, unique=True)

    job: Optional[str] = Field(default=None)
    job_chance_to_promo: float = Field(default=1.00)

    training: Optional[str] = Field(default=None)

    training_progress_id: Optional[int] = Field(default=None, foreign_key="trainingprogress.id", index=True)
    training_progress: Optional["TrainingProgress"] = Relationship(back_populates="user")

    stats_id: Optional[int] = Field(default=None, foreign_key="stats.id", index=True)
    stats: Optional["Stats"] = Relationship(back_populates="user")

    inventory_id: Optional[int] = Field(default=None, foreign_key="inventory.id", index=True)
    inventory: Optional["Inventory"] = Relationship(back_populates="user")

    corp_id: Optional[int] = Field(default=None, foreign_key="corporation.id", index=True)
    corporation: Optional["Corporation"] = Relationship(back_populates="employees")

    world_id: Optional[int] = Field(default=None, foreign_key="world.id", index=True)
    world: Optional["World"] = Relationship(back_populates="players")

    # I will clean this up in the future, for now I just cant be bothered. Not enough content yet
    sent_messages: List["PrivateMessage"] = Relationship(back_populates="sender",sa_relationship_kwargs={"primaryjoin": "User.id == PrivateMessage.sender_id"})
    received_messages: List["PrivateMessage"] = Relationship(back_populates="receiver",sa_relationship_kwargs={"primaryjoin": "User.id == PrivateMessage.receiver_id"})
    friend_requests_sent: List["FriendRequest"] = Relationship(back_populates="requester",sa_relationship_kwargs={"primaryjoin": "User.id == FriendRequest.requester_id"})
    friend_requests_received: List["FriendRequest"] = Relationship(back_populates="requestee",sa_relationship_kwargs={"primaryjoin": "User.id == FriendRequest.requestee_id"})
    friends: List["User"] = Relationship(back_populates="friends",link_model=FriendsLink,sa_relationship_kwargs={"primaryjoin": "User.id == FriendsLink.user2_id","secondaryjoin": "User.id == FriendsLink.user1_id"})





class PrivateMessage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    sender_id: int = Field(default=None, foreign_key="user.id")
    receiver_id: int = Field(default=None, foreign_key="user.id")
    content: str = Field()
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    sender: "User" = Relationship(back_populates="sent_messages",
                                  sa_relationship_kwargs={"primaryjoin": "PrivateMessage.sender_id == User.id"})
    receiver: "User" = Relationship(back_populates="received_messages",
                                    sa_relationship_kwargs={"primaryjoin": "PrivateMessage.receiver_id == User.id"})

class FriendRequest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    requester_id: int = Field(default=None, foreign_key="user.id")
    requestee_id: int = Field(default=None, foreign_key="user.id")
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships defined with explicit primary join conditions
    requester: "User" = Relationship(back_populates="friend_requests_sent",
                                     sa_relationship_kwargs={
                                         "primaryjoin": "FriendRequest.requester_id == User.id"
                                     })
    requestee: "User" = Relationship(back_populates="friend_requests_received",
                                     sa_relationship_kwargs={
                                         "primaryjoin": "FriendRequest.requestee_id == User.id"
                                     })
