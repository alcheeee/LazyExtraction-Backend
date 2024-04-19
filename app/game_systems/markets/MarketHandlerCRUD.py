from sqlmodel import Session, select
from app.models.models import User
from app.models.item_models import Items, GeneralMarket, BlackMarket
from app.database.UserCRUD import user_crud, engine
from app.utils.logger import MyLogger
from app.config import settings
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()


class BackendMarketHandler:
    def __init__(self, item_id, market_name, item_cost, sell_price):
        self.item_id = item_id
        self.market_name = market_name
        self.item_cost = item_cost
        self.sell_price = sell_price

    def add_item_to_market(self):
        with Session(engine) as session:
            transaction = session.begin()
            try:
                item = session.get(Items, self.item_id)
                if not item:
                    admin_log.error(f"Couldn't add item id {self.item_id} to {self.market_name}.")
                    raise ValueError(f"Item with id {self.item_id} not found.")

                existing_item = item.general_market_items.id
                if existing_item:
                    admin_log.error(f"{item.item_name} is already in the market")
                    raise ValueError(f"{item.item_name} is already in the market")


                market_item = {
                    "item_cost": self.item_cost,
                    "sell_price": self.sell_price,
                    "item_quality": item.quality.value,
                    "item_quantity": item.quantity,
                    "item_id": item.id
                }

                if self.market_name == 'General Market':
                    market_details = GeneralMarket(**market_item)
                    session.add(market_details)
                    session.commit()
                    admin_log.info(f"ADMIN ACTION - Added {item.item_name} to General Market.")
                    return True
                else:
                    admin_log.error(f"Market name {self.market_name} is not recognized.")
                    raise ValueError(f"Market name {self.market_name} is not recognized.")

            except Exception as e:
                session.rollback()
                admin_log.error(f"Failed to add item to market due to error: {e}")
                return False

