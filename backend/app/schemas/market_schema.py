from typing import Optional
from pydantic import BaseModel
from enum import Enum


class MarketNames(str, Enum):
    GeneralMarket = "general_market"
    BlackMarket = "black_market"
    Larry = "larry"
    Tommy = "tommy"

class Transactions(str, Enum):
    Posting = "posting"
    Buying = "buying"
    QuickSell = "quick_sell"
    Cancel = "cancel"

class MarketTransactionRequest(BaseModel):
    market_or_item_id: int
    market_name: Optional[MarketNames]
    transaction_type: Transactions
    item_cost: Optional[int]
    amount: int

