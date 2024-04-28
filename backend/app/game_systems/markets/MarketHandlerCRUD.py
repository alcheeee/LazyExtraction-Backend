from sqlmodel import select
from ...models.models import User
from ...models.item_models import Items, GeneralMarket, BlackMarket
from ..items.ItemStatsHandlerCRUD import ItemStatsHandler
from ...utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()


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
                admin_log.error(f"{item.item_name} is already in the market")
                raise Exception(f"{item.item_name} is already in the market")


            market_item = {
                "item_cost": self.item_cost,
                "sell_price": self.sell_price,
                "item_quality": item.quality.value,
                "item_quantity": item.quantity,
                "item_id": item.id
            }

            if self.market_name == 'General Market':
                market_details = GeneralMarket(**market_item)
                self.session.add(market_details)
                await self.session.commit()
                admin_log.info(f"ADMIN ACTION - Added {item.item_name} to General Market.")
                return True
            else:
                admin_log.error(f"Market name {self.market_name} is not recognized.")
                raise Exception(f"Market name {self.market_name} is not recognized.")

        except Exception as e:
            await self.session.rollback()
            admin_log.error(f"Failed to add item to market due to error: {e}")
            raise

class MarketItems:
    def __init__(self, session):
        self.session = session

    async def get_items(self):
        try:
            items = (await self.session.execute(select(GeneralMarket))).scalars().all()
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
            admin_log.error(f"Failed to get general market items: {str(e)}")
            raise