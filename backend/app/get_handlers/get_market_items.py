from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import (
    MarketCRUD,
    ItemsCRUD
)
from ..models import (
    Market,
    MarketItems,
    Items
)
from ..schemas import (
    GetMarketInfo,
    MarketInfo
)


class GetterMarketInfo:

    def __init__(self, market_info: GetMarketInfo, session: AsyncSession):
        self.market_info = market_info
        self.session = session
        self.market_crud = MarketCRUD(Market, session)
        self.items_crud = ItemsCRUD(Items, session)


    async def get_info(self):
        if self.market_info.getter_type == MarketInfo.SpecificItem:
            return await self.get_market_items()
        elif self.market_info.getter_type == MarketInfo.TenItems:
            return await self.get_market_items()
        else:
            raise Exception("Invalid Getter request")


    async def get_market_items(self):
        market_item_id = await self.market_crud.get_market_item_from_market_id(self.market_info.market_id)
        item = await self.session.get(MarketItems, market_item_id)
        return item


