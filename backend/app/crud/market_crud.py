from sqlalchemy import update, values, delete, select
from .base_crud import BaseCRUD
from ..models import (
    InventoryItem,
    Items,
    Market,
    MarketItems
)
from ..schemas import MarketTransactionRequest


class MarketCRUD(BaseCRUD):

    async def get_market_item_from_market_id(self, market_id: int):
        """
        :param market_id: MarketItems.id
        :return: MarketItems instance
        :raise ValueError
        """
        market_item = await self.session.get(MarketItems, market_id)
        if not market_item:
            raise ValueError("Item Not found")
        return market_item


    async def get_all_market_items_by_name(self, item_name: str, limit: int = 10, offset: int = 0):
        """
        :param item_name: Market.item_name
        :param limit: Number of items to return
        :param offset: Number of items to skip
        :return: List of MarketItems
        """
        query = (select(MarketItems)
                 .join(Market)
                 .where(Market.item_name == item_name)
                 .order_by(MarketItems.item_cost)
                 .limit(limit)
                 .offset(offset))
        result = await self.session.execute(query)
        return result.scalars().all()


    async def get_exact_market_item(self, details: MarketTransactionRequest, by_user: str = None):
        """
        :param details: MarketTransactionRequest
        :param by_user: Optional[User.username]
        :return: Optional[MarketItems instance]
        """
        query = select(MarketItems).where(
            MarketItems.item_id == details.item_id,
            MarketItems.item_cost == details.item_cost,
            MarketItems.by_user == by_user
        )
        result = await self.session.execute(query)
        return result.one_or_none()


    async def find_or_create_market(self, item_name):
        """
        :param item_name: Items.item_name
        :return: New/Updated Market
        """
        """ Find existing or create new market entry """
        market = await self.session.execute(
            select(Market).where(
                Market.item_name == item_name
            )
        )
        market = market.scalars().first()

        if not market:
            market = Market(
                item_name=item_name
            )
            self.session.add(market)
            await self.session.flush()

        return market