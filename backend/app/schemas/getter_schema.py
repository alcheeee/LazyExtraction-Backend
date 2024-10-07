from typing import Optional
from pydantic import BaseModel
from enum import Enum


class UserInfoNeeded(str, Enum):
    All = "all"
    Stats = "stats"
    Inventory = "inventory"
    InventoryItems = "inventory_items"


class MarketInfo(str, Enum):
    TenItems = "10_items"
    SpecificItem = "specific_item"


class GetMarketInfo(BaseModel):
    getter_type: MarketInfo = MarketInfo.TenItems
    market_id: Optional[int]

