from sqlalchemy import update, values, delete
from .BaseCRUD import BaseCRUD
from ..models.models import InventoryItem
from ..models.item_models import Items, MarketItems
from ..schemas.market_schema import MarketNames


class MarketCRUD(BaseCRUD):

    async def get_item_info_for_purchase(self, market_item_id: int):
        query = select(
            MarketItems.item_id,
            MarketItems.item_cost,
            MarketItems.market_name,
            MarketItems.item_quantity
        ).where(MarketItems.id == market_item_id)
        result = await self.session.execute(query)
        return result.fetchone()