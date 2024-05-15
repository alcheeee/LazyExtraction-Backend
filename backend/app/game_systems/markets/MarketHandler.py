from sqlalchemy.ext.asyncio import AsyncSession

from ...models.models import User, Inventory
from ...models.item_models import Items, MarketItems
from ...schemas.market_schema import MarketTransactionRequest, Transactions

from ...crud.MarketCRUD import MarketCRUD
from ...crud.ItemCRUD import ItemsCRUD
from ...crud.UserCRUD import UserCRUD
from ...crud.UserInventoryCRUD import UserInventoryCRUD

from ...utils.logger import MyLogger
error_log = MyLogger.errors()
game_log = MyLogger.game()


class MarketTransactionHandler:
    def __init__(self, request: MarketTransactionRequest, user_id: int, session: AsyncSession, admin_request=False):
        self.admin_request = admin_request
        self.request = request
        self.user_id = user_id
        self.session = session
        self.market_crud = MarketCRUD(MarketItems, session)
        self.item_crud = ItemsCRUD(Items, session)
        self.inventory_crud = UserInventoryCRUD(User, session)
        self.user_crud = UserCRUD(User, session)
        self.transaction = request.transaction_type


    async def market_transaction(self):
        posting_details = {
            "item_id": self.request.market_or_item_id,
            "market_name": self.request.market_name,
            "item_cost": self.request.item_cost,
            "amount": abs(self.request.amount)
        }
        quick_sell_details = {
            "market_id": self.request.market_or_item_id,
            "amount": abs(self.request.amount)
        }
        buying_details = {
            "market_id": self.request.market_or_item_id,
            "amount": abs(self.request.amount)
        }
        if self.transaction == Transactions.QuickSell:
            result = await self.quick_sell(quick_sell_details)
            return result

        elif self.transaction == Transactions.Buying:
            result = await self.buying(buying_details)
            return result

        elif self.transaction == Transactions.Posting:
            result = await self.posting(posting_details)
            return result
        else:
            raise ValueError("Invalid Transaction")

    async def posting(self, posting_details: dict):
        item_name = await self.check_item_name(posting_details['item_id'])
        market = await self.market_crud.find_or_create_market(item_name, posting_details['market_name'])

        if not self.admin_request:
            inv_item, user_inv_id = await self.get_item_if_user_has_item(posting_details['item_id'])
            await self.inventory_crud.update_user_inventory_item(
                user_inv_id,
                posting_details['item_id'],
                -int(posting_details['amount']),
                inventory_item=inv_item
            )

        by_user = 'Market' if self.admin_request else await self.user_crud.get_user_field_from_id(self.user_id, 'username')
        new_market_item = MarketItems(
            main_market_post_id=market.id,
            item_id=posting_details['item_id'],
            item_cost=posting_details['item_cost'],
            item_quantity=posting_details['amount'],
            by_user=by_user,
        )
        self.session.add(new_market_item)
        return "Item Posted Successfully"


    async def buying(self, buying_details: dict):
        market_item = await self.get_market_item(buying_details['market_id'])
        if market_item.item_quantity < buying_details['amount']:
            raise ValueError("Not enough stock")

        user_inventory = await self.get_user_inventory()
        total_cost = market_item.item_cost * buying_details['amount']
        if user_inventory.bank < total_cost:
            raise ValueError("Not enough money to purchase that item")

        market_item.item_quantity -= buying_details['amount']
        user_inventory.bank -= total_cost

        await self.inventory_crud.update_user_inventory_item(
            user_inventory.id,
            market_item.item_id,
            buying_details['amount']
        )
        if market_item.item_quantity <= 0:
            await self.session.delete(market_item)
        return "Purchase successful"


    async def quick_sell(self, selling_details: dict):

        pass


    async def get_market_item(self, market_id: int):
        market_item = await self.market_crud.get_market_item_from_market_id(market_id)
        if not market_item:
            raise ValueError("That item is not available")
        return market_item


    async def get_user_inventory(self):
        user_inv_id = await self.inventory_crud.get_user_inventory_id_by_userid(self.user_id)
        user_inventory = await self.session.get(Inventory, user_inv_id)
        if user_inventory is None:
            raise Exception("User inventory could not be located")
        return user_inventory

    async def check_item_name(self, item_id: int):
        item_name = await self.item_crud.get_item_name_by_id(item_id)
        if not item_name:
            raise ValueError("Could not find that item")
        return item_name

    async def get_item_if_user_has_item(self, item_id: int):
        user_inv_id = await self.inventory_crud.get_user_inventory_id_by_userid(self.user_id)
        if not user_inv_id:
            raise Exception("Error finding users inventory")
        inventory_item = await self.inventory_crud.get_user_inventory_item(user_inv_id, item_id)
        if not inventory_item:
            raise ValueError("You don't have that item")
        return inventory_item, user_inv_id





