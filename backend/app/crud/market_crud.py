from sqlalchemy import update, values, delete, select
from .base_crud import BaseCRUD
from ..models import (
    InventoryItem,
    Items,
    Market,
    MarketItems
)
from ..schemas import MarketNames, MarketTransactionRequest


class MarketCRUD(BaseCRUD):

    async def get_market_item_from_market_id(self, market_id: int):
        """
        :param market_id: MarketItems.id
        :return: MarketItems instance
        :raise ValueError
        """
        market_item = await self.session.get(MarketItems, market_id)
        if not market_item:
            raise ValueError("That item is not available")
        return market_item


    async def get_exact_market_item(self, details: MarketTransactionRequest, by_user: str = None):
        """
        :param details: MarketTransactionRequest
        :param by_user: Optional[User.username]
        :return: Optional[MarketItems instance]
        """
        query = select(MarketItems).where(
            MarketItems.item_id == details.item_id,
            MarketItems.market_name == details.market_name,
            MarketItems.item_cost == details.item_cost,
            MarketItems.by_user == by_user
        )
        result = await self.session.execute(query)
        return result.one_or_none()



    async def find_or_create_market(self, item_name, market_name):
        """
        :param item_name: Items.item_name
        :param market_name: MarketNames Enum
        :return: New/Updated Market
        """
        """ Find existing or create new market entry """
        market = await self.session.execute(
            select(Market).where(
                Market.item_name == item_name,
                Market.market_name == market_name
            )
        )
        market = market.scalars().first()

        if not market:
            market = Market(
                item_name=item_name,
                market_name=market_name
            )
            self.session.add(market)
            await self.session.flush()

        return market