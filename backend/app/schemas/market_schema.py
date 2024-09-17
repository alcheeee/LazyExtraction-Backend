from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Transactions(str, Enum):
    Posting = "posting"
    Buying = "buying"
    QuickSell = "quick_sell"
    Cancel = "cancel"

class MarketTransactionRequest(BaseModel):
    market_item_id: Optional[int] = None
    inventory_item_id: Optional[int] = None
    transaction_type: Transactions
    item_cost: Optional[int] = None
    amount: Optional[int] = None
