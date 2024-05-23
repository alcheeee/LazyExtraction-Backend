from typing import Optional
from pydantic import BaseModel
from enum import Enum


class NPCNames(str, Enum):
    Larry = "larry"
    Tommy = "tommy"

