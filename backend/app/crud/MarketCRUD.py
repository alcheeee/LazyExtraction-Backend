from sqlalchemy import update, values, delete, select
from .BaseCRUD import BaseCRUD
from ..models.models import InventoryItem
from ..models.item_models import Items, MarketItems, Market
from ..schemas.market_schema import MarketNames, MarketTransactionRequest


class MarketCRUD(BaseCRUD):

    async def get_market_item_from_item_id(self, market_id: int):
        market_item = await self.session.get(MarketItems, market_id)
        return market_item


    async def get_exact_market_item(self, details: MarketTransactionRequest, by_user: str = None):
        query = select(MarketItems).where(
            MarketItems.item_id == details.item_id,
            MarketItems.market_name == details.market_name,
            MarketItems.item_cost == details.item_cost,
            MarketItems.by_user == by_user
        )
        result = await self.session.execute(query)
        return result.one_or_none()


    async def find_or_create_market(self, item_name, market_name):
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