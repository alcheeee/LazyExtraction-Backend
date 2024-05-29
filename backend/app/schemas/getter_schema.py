from pydantic import BaseModel
from enum import Enum


class UserInfoNeeded(str, Enum):
    Stats = "stats"
    Inventory = "inventory"
    InventoryItems = "inventory_items"


