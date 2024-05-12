from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from ...models.models import User
from ...models.item_models import Items, MarketItems
from ...schemas.market_schema import MarketNames, MarketTransactionRequest
from ...schemas.item_schema import filter_item_stats

from ..items.ItemStatsHandlerCRUD import ItemStatsHandler
from ...crud.MarketCRUD import MarketCRUD
from ...crud.ItemCRUD import ItemsCRUD
from ...crud.UserInventoryCRUD import UserInventoryCRUD

from ...utils.logger import MyLogger
error_log = MyLogger.errors()
game_log = MyLogger.game()


class MarketTransactionHandler:
    def __init__(self, request: MarketTransactionRequest, user_id: int, session: AsyncSession):
        self.request = request
        self.user_id = user_id
        self.session = session
        self.market_crud = MarketCRUD(None, session)
        self.item_crud = ItemsCRUD(None, session)
        self.inventory_crud = UserInventoryCRUD(None, session)

    async def item_check(self):
        market_item = await self.market_crud.get_item_info_for_purchase(self.request.market_item_id)
        if not market_item:
            raise Exception("Item not found")
        if market_item.item_quantity < self.request.quantity:
            raise ValueError("Not enough in stock")
        return market_item

    async def market_purchase(self):
        market_item = await self.item_check()
        total_cost = market_item.item_cost * self.request.quantity
        user_inventory = await self.session.get(User.inventory, User.id == self.user_id)

        if user_inventory.bank < total_cost:
            raise ValueError("You can't afford that item")

        user_inventory.bank -= total_cost
        market_item.item_quantity -= self.request.quantity

        await self.inventory_crud.update_user_inventory_item(user_inventory.id, market_item.item_id, self.request.quantity)

    async def market_sell(self):
        pass



class BackendMarketHandler:
    def __init__(self, item_id, market_name, item_cost, sell_price, session):
        self.item_id = item_id
        self.market_name = market_name
        self.item_cost = item_cost
        self.sell_price = sell_price
        self.session = session

    async def add_item_to_market(self):
        try:
            item = await self.session.get(Items, self.item_id)
            if not item:
                raise Exception(f"Item with id {self.item_id} not found.")

            existing_item = item.general_market_items.id if item.general_market_items else None
            if existing_item:
                raise Exception(f"{item.item_name} is already in the market")

            market_item = {
                "item_cost": self.item_cost,
                "sell_price": self.sell_price,
                "item_quality": item.quality.value,
                "item_quantity": item.quantity,
                "item_id": item.id
            }

            if self.market_name == 'General Market':
                market_details = MarketItems(**market_item)
                self.session.add(market_details)
                await self.session.commit()
                admin_log.info(f"ADMIN ACTION - Added {item.item_name} to General Market.")
                return True
            else:
                raise Exception(f"Market name {self.market_name} is not recognized.")

        except Exception as e:
            await self.session.rollback()
            error_log.error(f"Failed to add item to market due to error: {e}")
            raise

class MarketItems:
    def __init__(self, session):
        self.session = session

    async def get_items(self):
        try:
            items = (await self.session.execute(select(MarketItems))).scalars().all()
            item_details = []
            for item in items:
                main_item = await self.session.get(Items, item.item_id)
                item_info = {
                    "item_id": item.item_id,
                    "item_name": main_item.item_name,
                    "item_quality": main_item.quality,
                    "quantity": item.item_quantity,
                    "illegal": main_item.illegal,
                    "category": main_item.category.value,
                    "slot_type": None,
                    "equipped_slot": None,
                    "item_cost": item.item_cost,
                    "sell_price": item.sell_price,
                }
                if main_item.category.value in ['Clothing', 'Weapon']:
                    item_info["slot_type"] = (main_item.clothing_details.clothing_type if
                                              main_item.category.value == 'Clothing' else 'Weapon')
                item_stats_handler = ItemStatsHandler(0, main_item.id, self.session)
                check_for_stats = item_stats_handler.get_item_stats_json(main_item)
                if check_for_stats:
                    item_info["stats"] = check_for_stats

                item_details.append(item_info)
            return item_details
        except Exception as e:
            error_log.error(f"Failed to get general market items: {str(e)}")
            raise