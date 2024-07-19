from enum import Enum
from pydantic import BaseModel


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
    id: int = 0


class WorldCreator(BaseModel):
    world_name: WorldNames
    node_json: str



