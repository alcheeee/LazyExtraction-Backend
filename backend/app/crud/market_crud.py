from typing import List
from sqlalchemy import update, values, delete, select
from .base_crud import BaseCRUD
from ..models import (
    InventoryItem,
    Items,
    MarketItems
)
from app.schemas import MarketTransactionRequest


class MarketCRUD(BaseCRUD):

    async def get_market_item_from_market_id(self, market_id: int):
        """
        :param market_id: MarketItems.id
        :return: MarketItems
        :raise ValueError
        """
        market_item = await self.session.get(MarketItems, market_id)
        if not market_item:
            raise LookupError("Item not found")
        return market_item

    async def get_all_market_items_by_name(
            self, item_name: str, limit: int = 10, offset: int = 0
    ) -> List[MarketItems] | None:
        """
        :param item_name: Items.item_name
        :param limit: Number of items to return
        :param offset: Number of items to skip
        :return: List of MarketItems | None
        """
        query = (select(MarketItems)
                 .where(MarketItems.item_name == item_name)
                 .order_by(MarketItems.item_cost)
                 .limit(limit)
                 .offset(offset))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_exact_market_item(self, market_item_id: int) -> MarketItems | None:
        """
        :param market_item_id: MarketItems.id
        :return: MarketItems | None
        """
        return await self.session.get(MarketItems, market_item_id)