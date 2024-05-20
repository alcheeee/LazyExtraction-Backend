import tenacity
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.market_schema import MarketTransactionRequest, Transactions

from ...crud import (
    MarketCRUD,
    ItemsCRUD,
    UserCRUD,
    UserInventoryCRUD
)
from ...models import (
    User,
    Items,
    MarketItems
)


class MarketTransactionHandler:
    def __init__(self, request: MarketTransactionRequest, user_id: int, session: AsyncSession, admin_request=False):
        self.admin_request = admin_request
        self.request = request
        self.user_id = user_id
        self.session = session
        self.market_crud = MarketCRUD(MarketItems, session)
        self.item_crud = ItemsCRUD(Items, session)
        self.inv_crud = UserInventoryCRUD(User, session)
        self.user_crud = UserCRUD(User, session)
        self.transaction = request.transaction_type


    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def market_transaction(self):
        """
        Handler for all market_transactions
        :return: Transaction complete or ValueError
        """
        transaction_mapping = {
            Transactions.Cancel: {
                "method": self.cancel_market_post,
                "details": {"market_id": self.request.market_or_item_id}
            },
            Transactions.QuickSell: {
                "method": self.quick_sell,
                "details": {
                    "item_id": self.request.market_or_item_id,
                    "amount": abs(self.request.amount)
                }
            },
            Transactions.Buying: {
                "method": self.buying,
                "details": {
                    "market_id": self.request.market_or_item_id,
                    "amount": abs(self.request.amount)
                }
            },
            Transactions.Posting: {
                "method": self.posting,
                "details": {
                    "item_id": self.request.market_or_item_id,
                    "market_name": self.request.market_name,
                    "item_cost": self.request.item_cost,
                    "amount": abs(self.request.amount)
                }
            }
        }
        if self.transaction in transaction_mapping:
            transaction = transaction_mapping[self.transaction]
            result = await transaction["method"](transaction["details"])
            return result
        else:
            raise ValueError("Invalid Transaction")


    async def posting(self, posting_details: dict):
        """
        :param posting_details: item_id, market_name, item_cost, amount
        :return: Successful post or error
        """
        item_name = await self.item_crud.get_item_name_by_id(posting_details['item_id'])
        market = await self.market_crud.find_or_create_market(item_name, posting_details['market_name'])

        # Admin requests check (for creating Permanent-Market items)
        if not self.admin_request:
            inv_item = await self.inv_crud.get_inventory_item_by_userid(self.user_id, posting_details['item_id'])
            await self.inv_crud.update_user_inventory_item(
                0,
                posting_details['item_id'],
                -int(posting_details['amount']),
                inventory_item=inv_item
            )

        # If Admin post it'll just be under Market
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
        # Getting market item instance and Purchasers username
        market_item = await self.market_crud.get_market_item_from_market_id(buying_details['market_id'])
        current_user_username = await self.user_crud.get_user_field_from_id(self.user_id, 'username')

        # Quantity and self-purchasing checks
        if market_item.by_user == current_user_username:
            raise ValueError("You can't buy your own items")
        if market_item.item_quantity < buying_details['amount']:
            raise ValueError("Not enough stock")

        # Getting inventory_id and balance for balance check
        user_inv_id, user_bank = await self.inv_crud.get_user_bank_from_userid(self.user_id)
        total_cost = market_item.item_cost * buying_details['amount']
        if user_bank < total_cost:
            raise ValueError("Not enough money to purchase that item")

        # Checks passed, perform operation
        market_item.item_quantity -= buying_details['amount']
        adjusted_balance = user_bank - total_cost

        await self.inv_crud.update_bank_balance(user_inv_id, adjusted_balance)
        await self.inv_crud.update_bank_balance_by_username(market_item.by_user, total_cost)
        await self.inv_crud.update_user_inventory_item(
            user_inv_id,
            market_item.item_id,
            buying_details['amount']
        )
        if market_item.item_quantity <= 0:
            await self.session.delete(market_item)
        return "Purchase successful"


    async def quick_sell(self, selling_details: dict):
        # Checks
        inv_item = await self.inv_crud.get_inventory_item_by_userid(self.user_id, selling_details['item_id'])
        if inv_item.quantity < selling_details['amount']:
            raise ValueError("Invalid amount")

        # Getting fields for adjustments
        user_inv_id, user_bank = await self.inv_crud.get_user_bank_from_userid(self.user_id)
        quick_sell_value = await self.item_crud.get_item_field_from_id(selling_details['item_id'], 'quick_sell')

        # Balance Calculations
        total_amount = quick_sell_value * selling_details['amount']
        new_bank_balance = user_bank + total_amount

        # Perform operation
        await self.inv_crud.update_bank_balance(user_inv_id, new_bank_balance)
        await self.inv_crud.update_user_inventory_item(
            user_inv_id,
            selling_details['item_id'],
            -int(selling_details['amount']),
            inventory_item=inv_item
        )
        return "Quick-Sell Successful"


    async def cancel_market_post(self, cancel_details):
        current_user_username = await self.user_crud.get_user_field_from_id(self.user_id, 'username')
        market_item = await self.market_crud.get_market_item_from_market_id(cancel_details['market_id'])

        if current_user_username == market_item.by_user:
            user_inv_id = await self.inv_crud.get_user_inventory_id_by_userid(self.user_id)
            await self.inv_crud.update_user_inventory_item(
                user_inv_id,
                market_item.item_id,
                market_item.item_quantity
            )
            await self.session.delete(market_item)
            return "Item taken off the market"
        raise ValueError("That's not your item")



