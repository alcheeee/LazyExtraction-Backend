import tenacity
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import MarketTransactionRequest, Transactions

from ...crud import (
    MarketCRUD,
    ItemsCRUD,
    UserCRUD,
    UserInventoryCRUD
)
from ...models import (
    User,
    Items,
    MarketItems,
    Inventory,
    InventoryItem
)


class MarketTransactionHandler:
    def __init__(
            self,
            request: MarketTransactionRequest,
            user_data: dict,
            session: AsyncSession,
            admin_request=False
    ):
        self.admin_request = admin_request
        self.transaction_data = request
        self.user_id = int(user_data['user']['user_id'])
        self.username = user_data['user']['username']
        self.session = session
        self.market_crud = MarketCRUD(MarketItems, session)
        self.item_crud = ItemsCRUD(Items, session)
        self.inv_crud = UserInventoryCRUD(User, session)

    async def market_transaction(self):
        """
        Handler for all market_transactions
        :return: Transaction complete or ValueError
        """
        match self.transaction_data.transaction_type:
            case Transactions.Cancel:
                return await self.cancel_market_post(self.transaction_data.market_item_id)
            case Transactions.QuickSell:
                return await self.quick_sell(self.transaction_data.inventory_item_id, self.transaction_data.amount)
            case Transactions.Buying:
                return await self.buying(self.transaction_data.market_item_id, self.transaction_data.amount)
            case Transactions.Posting:
                return await self.posting(self.transaction_data.inventory_item_id, self.transaction_data.amount, self.transaction_data.item_cost)
            case _:
                raise ValueError("Invalid Transaction")

    async def posting(self, inventory_item_id: int, amount: int, item_cost: int):
        data = {}
        inventory_item = await self.session.get(InventoryItem, inventory_item_id)
        if not inventory_item:
            raise LookupError("Inventory item not found")

        data['inventory-item'] = inventory_item

        # Admin requests check (for creating Permanent-Market items)
        if not self.admin_request:
            await self.inv_crud.update_any_inventory_quantity(
                self.user_id, -amount, inventory_item  # type: ignore
            )

        market = await self.market_crud.find_or_create_market(inventory_item.item.item_name)

        # If Admin post it'll just be under Market
        by_user = 'Market' if self.admin_request else self.username
        # TODO : NPCs rather than 'Market'
        new_market_item = MarketItems(
            main_market_post_id=market.id,
            item_name=inventory_item.item_name,
            item_id=inventory_item.item_id,
            quick_sell_value=inventory_item.quick_sell_value,
            item_cost=item_cost,
            item_quantity=amount,
            by_user=by_user,
            is_modified=inventory_item.is_modified,
            modifications=inventory_item.modifications
        )
        self.session.add(new_market_item)
        data['market-item'] = new_market_item
        return "Item Posted Successfully", data


    async def buying(self, market_item_id: int, amount: int):
        data = {}
        # Getting market item instance and Purchasers username
        market_item = await self.market_crud.get_market_item_from_market_id(market_item_id)
        if not market_item:
            raise LookupError("Market item not found")

        data['market-item'] = market_item

        # Quantity and self-purchasing checks
        if market_item.by_user == self.username:
            raise ValueError("You can't buy your own items")

        if market_item.item_quantity < amount:
            raise ValueError("Not enough stock")

        # Getting inventory_id and balance for balance check
        user_inv_id, user_bank = await self.inv_crud.get_user_bank_from_userid(self.user_id)
        total_cost = market_item.item_cost * amount
        if user_bank < total_cost:
            raise ValueError("Not enough money to purchase that item")

        # Checks passed, perform operation
        market_item.item_quantity -= amount
        adjusted_balance = user_bank - total_cost

        await self.inv_crud.update_bank_balance(user_inv_id, adjusted_balance)
        await self.inv_crud.update_bank_balance_by_username(market_item.by_user, total_cost)

        # Handles the case where the item is modified
        buyer_inventory_item = await self.inv_crud.get_inventory_item_by_item_id(
            user_inv_id,
            market_item.item_id
        )
        if buyer_inventory_item and not market_item.is_modified:
            await self.inv_crud.update_any_inventory_quantity(
                self.user_id, amount, buyer_inventory_item
            )
            data['inventory-item'] = buyer_inventory_item
        else:
            new_inventory_item = InventoryItem(
                item_name=market_item.item_name,
                quick_sell_value=market_item.quick_sell_value,
                inventory_id=user_inv_id,
                item_id=market_item.inventory_item.item_id,
                amount_in_stash=amount,
                is_modified=market_item.is_modified,
                modifications=market_item.modifications
            )
            self.session.add(new_inventory_item)
            data['inventory-item'] = new_inventory_item

        if market_item.item_quantity <= 0:
            await self.session.delete(market_item)

        data['bank-update'] = adjusted_balance

        return "Purchase successful", data


    async def quick_sell(self, inventory_item_id: int, amount: int):
        inventory_item = await self.session.get(InventoryItem, inventory_item_id)
        if not inventory_item:
            raise LookupError("Inventory item not found")

        if inventory_item.amount_in_stash < amount:
            raise ValueError("Invalid amount")

        user_inv_id, user_bank = await self.inv_crud.get_user_bank_from_userid(self.user_id)
        quick_sell_value = inventory_item.quick_sell_value

        total_amount = quick_sell_value * amount
        new_bank_balance = user_bank + total_amount

        await self.inv_crud.update_bank_balance(user_inv_id, new_bank_balance)
        await self.inv_crud.update_any_inventory_quantity(
            self.user_id, -amount, inventory_item  # type: ignore
        )

        return "Quick-Sell Successful", {'bank': new_bank_balance}


    async def cancel_market_post(self, market_item_id: int):
        data = {}
        market_item = await self.market_crud.get_market_item_from_market_id(market_item_id)
        if not market_item:
            raise LookupError("Market item not found")

        data['market-item'] = market_item

        if self.username != market_item.by_user:
            raise ValueError("That's not your item")

        user_inv_id = await self.inv_crud.get_user_inventory_id_by_userid(self.user_id)

        # Handle the case where the item might be modified
        inventory_item = await self.inv_crud.get_inventory_item_by_item_id(user_inv_id, market_item.item_id)

        if inventory_item and not market_item.is_modified:
            await self.inv_crud.update_any_inventory_quantity(
                self.user_id, market_item.item_quantity, inventory_item  # type: ignore
            )
        else:
            new_inventory_item = InventoryItem(
                item_name=market_item.item_name,
                quick_sell_value=market_item.quick_sell_value,
                inventory_id=user_inv_id,
                item_id=market_item.item_id,
                amount_in_stash=market_item.item_quantity,
                is_modified=market_item.is_modified,
                modifications=market_item.modifications
            )
            self.session.add(new_inventory_item)
            data['inventory-item'] = new_inventory_item

        await self.session.delete(market_item)
        return "Item taken off the market", data



