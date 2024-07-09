from enum import Enum
from pydantic import BaseModel


class NewCrewInfo(BaseModel):
    name: str
    private: bool = False


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
