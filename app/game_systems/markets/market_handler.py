from app.models.models import User, Inventory
from app.models.item_models import Items, GeneralMarket, BlackMarket
from app.database.UserCRUD import user_crud, engine


class BackendMarketHandler:
    def __init__(self, item_id, market_name):
        self.item_id = item_id
        self.market_name = market_name

    def get_market(self):
        pass

