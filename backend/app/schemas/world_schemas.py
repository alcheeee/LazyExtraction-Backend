from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, UUID4


class WorldTier(Enum):
    Tier1 = 'Tier 1'
    Tier2 = 'Tier 2'
    Tier3 = 'Tier 3'


class WorldNames(str, Enum):
    Forest = "Forest"
    Laboratory = "Laboratory"
    MilitaryBase = "Military Base"


class InteractionTypes(str, Enum):
    Pickup = "pickup"
    Traverse = "traverse"
    Extract = "extract"


class RoomInteraction(BaseModel):
    action: InteractionTypes = InteractionTypes.Pickup
    id: UUID4


class WorldCreator(BaseModel):
    world_name: WorldNames
    world_tier: WorldTier = WorldTier.Tier1
    node_json: str



