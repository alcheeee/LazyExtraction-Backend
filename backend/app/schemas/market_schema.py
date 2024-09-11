from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Transactions(str, Enum):
    Posting = "posting"
    Buying = "buying"
    QuickSell = "quick_sell"
    Cancel = "cancel"

class MarketTransactionRequest(BaseModel):
    market_or_item_id: int
    transaction_type: Transactions
    item_cost: Optional[int]
    amount: int

