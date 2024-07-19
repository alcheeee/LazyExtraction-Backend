from typing import Optional
from enum import Enum
from pydantic import BaseModel


class NewCrewInfo(BaseModel):
    name: str
    private: bool = False

class AddRemoveCrewRequest(BaseModel):
    user_to_add_remove: str
    crew_id: int

class CrewDefaults:
    items = [
        "Polymer",
        "Electronic Parts",
        "Scrap Metal"
    ]
    upgrades = [
        "better_box",
        "max_players"
    ]
