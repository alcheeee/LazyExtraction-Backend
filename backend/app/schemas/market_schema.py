from pydantic import BaseModel
from enum import Enum


class MarketNames(str, Enum):
    GeneralMarket = "general_market"
    BlackMarket = "black_market"


class MarketTransactionRequest(BaseModel):
    market_item_id: int
    market_name: MarketNames
    quantity: int
