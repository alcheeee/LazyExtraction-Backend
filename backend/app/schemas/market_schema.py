from typing import Optional
from pydantic import BaseModel
from enum import Enum


class MarketNames(str, Enum):
    GeneralMarket = "general_market"
    BlackMarket = "black_market"

class Transactions(str, Enum):
    Posting = "posting"
    Buying = "buying"
    Selling = "selling"

class MarketTransactionRequest(BaseModel):
    market_or_item_id: int
    market_name: MarketNames
    transaction_type: Transactions
    item_cost: Optional[int]
    amount: int

    sell_price: Optional[int] = None    # Only for In-Game items by admins
    quick_sell: Optional[bool] = False  # Only for In-Game items by admins

