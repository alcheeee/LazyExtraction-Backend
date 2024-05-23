from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class WorldTier(Enum):
    Tier1 = 'Tier 1'
    Tier2 = 'Tier 2'
    Tier3 = 'Tier 3'


class WorldNames(str, Enum):
    Forest = "forest"
    Laboratory = "laboratory"
    MilitaryBase = "military_base"


class WorldInteraction(BaseModel):
    """For node traversal"""
    pass


class RoomInteraction(BaseModel):
    """For interacting with in-room options (items, pve, ect)"""
    pass


class WorldCreator(BaseModel):
    world_tier: WorldTier = WorldTier.Tier1
    node_json: str
    max_players: int = 8



