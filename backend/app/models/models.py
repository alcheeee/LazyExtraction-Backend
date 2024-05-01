from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class Stats(SQLModel, table=True):
    """
    Stats Table for Users, linked by id
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    level: float = Field(default=1.00)
    reputation: int = Field(default=1)
    job: Optional[str] = Field(default=None)
    education: Optional[str] = Field(default=None)
    max_energy: int = Field(default=100)
    damage: int = Field(default=1)
    evasiveness: float = Field(default=1.00)
    health: int = Field(default=100)
    luck: float = Field(default=1.00)
    strength: float = Field(default=1.00)
    knowledge: float = Field(default=1.00)
    user_id: int = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="stats")
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
    bank: int = Field(default=1000)
    energy: int = Field(default=100)
    equipped_weapon_id: Optional[int] = Field(default=None)
    equipped_mask_id: Optional[int] = Field(default=None)
    equipped_body_id: Optional[int] = Field(default=None)
    equipped_legs_id: Optional[int] = Field(default=None)
    items: List["InventoryItem"] = Relationship(back_populates="inventory")
    user_id: int = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="inventory")


class InventoryItem(SQLModel, table=True):
    """
    Represents individual items within a user's inventory.
    """
    id: int = Field(default=None, primary_key=True)
    inventory_id: int = Field(default=None, foreign_key="inventory.id")
    item_id: int = Field(default=None, foreign_key="items.id")
    quantity: int
    inventory: Optional["Inventory"] = Relationship(back_populates="items")
    item: Optional["Items"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


class FriendsLink(SQLModel, table=True):
    user1_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    user2_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)

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
    password: str
    email: str = Field(index=True)

    corp_id: Optional[int] = Field(default=None, foreign_key="corporations.id")
    corporation: Optional["Corporations"] = Relationship(back_populates="employees")
    stats: Stats = Relationship(back_populates="user")
    inventory: Inventory = Relationship(back_populates="user")
    sent_messages: List["PrivateMessage"] = Relationship(back_populates="sender",sa_relationship_kwargs={"primaryjoin": "User.id == PrivateMessage.sender_id"})
    received_messages: List["PrivateMessage"] = Relationship(back_populates="receiver",sa_relationship_kwargs={"primaryjoin": "User.id == PrivateMessage.receiver_id"})
    friend_requests_sent: List["FriendRequest"] = Relationship(back_populates="requester",sa_relationship_kwargs={"primaryjoin": "User.id == FriendRequest.requester_id"})
    friend_requests_received: List["FriendRequest"] = Relationship(back_populates="requestee",sa_relationship_kwargs={"primaryjoin": "User.id == FriendRequest.requestee_id"})
    friends: List["User"] = Relationship(back_populates="friends",link_model=FriendsLink,sa_relationship_kwargs={"primaryjoin": "User.id == FriendsLink.user2_id","secondaryjoin": "User.id == FriendsLink.user1_id"})

