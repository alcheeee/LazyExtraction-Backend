import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.game_systems.markets.market_handler import MarketTransactionHandler
from app.schemas import MarketTransactionRequest, Transactions
from app.models import MarketItems, InventoryItem


@pytest.fixture
def mock_bank_crud():
    with patch('app.crud.user_bank_crud.UserBankingCRUD') as mock:
        yield mock.return_value


@pytest.fixture
def mock_market_crud():
    with patch('app.crud.market_crud.MarketCRUD') as mock:
        yield mock.return_value


@pytest.fixture
def mock_market_item():
    item = Mock(spec=MarketItems)
    item.by_user = "seller"
    item.item_quantity = 10
    item.item_cost = 100
    item.item_name = "Test Item"
    item.quick_sell_value = 50
    item.item_id = 1
    item.is_modified = False
    item.modifications = None
    item.inventory_item = Mock(item_id=1)
    return item


@pytest.fixture
def handler(mock_session, mock_market_crud, mock_items_crud, mock_user_inv_crud, mock_bank_crud):
    request = MarketTransactionRequest(
        transaction_type=Transactions.Posting,
        inventory_item_id=1,
        amount=5,
        item_cost=100,
        market_item_id=None
    )
    user_data = {'user': {'user_id': '1', 'username': 'testuser'}}
    handler = MarketTransactionHandler(request, user_data, mock_session)
    handler.market_crud = mock_market_crud
    handler.item_crud = mock_items_crud
    handler.inv_crud = mock_user_inv_crud
    handler.banking_crud = mock_bank_crud
    handler.inv_crud.update_any_inventory_quantity = AsyncMock()
    handler.banking_crud.get_user_bank_from_userid = AsyncMock(return_value=())
    handler.banking_crud.update_bank_balance = AsyncMock()
    handler.banking_crud.update_bank_balance_by_username = AsyncMock()
    return handler



class TestMarketHandler:

    @pytest.mark.parametrize("transaction_type, method_name", [
        (Transactions.Posting, "posting"),
        (Transactions.Buying, "buying"),
        (Transactions.QuickSell, "quick_sell"),
        (Transactions.Cancel, "cancel_market_post"),
    ])
    async def test_market_transaction(self, transaction_type, method_name, handler):
        handler.transaction_data.transaction_type = transaction_type
        handler.transaction_data.market_item_id = 1
        handler.transaction_data.inventory_item_id = 1
        handler.transaction_data.amount = 5
        handler.transaction_data.item_cost = 100
        mock_method = AsyncMock(return_value=("Success", {}))
        setattr(handler, method_name, mock_method)
        result = await handler.market_transaction()
        assert result == ("Success", {})
        mock_method.assert_awaited_once()


    async def test_posting(self, handler, mock_session, mock_inventory_item):
        mock_session.get = AsyncMock(return_value=mock_inventory_item)
        result, data = await handler.posting(1, 5, 100)
        assert result == "Item Posted Successfully"
        assert 'inventory-item' in data
        assert 'market-item' in data
        handler.inv_crud.update_any_inventory_quantity.assert_awaited_once_with(1, -5, mock_inventory_item)
        mock_session.add.assert_called_once()


    async def test_buying(self, handler, mock_session, mock_market_item):
        handler.market_crud.get_market_item_from_market_id = AsyncMock(return_value=mock_market_item)
        handler.banking_crud.get_user_bank_from_userid = AsyncMock(return_value=(1, 1000))
        handler.inv_crud.get_inventory_item_by_item_id = AsyncMock(return_value=None)
        result, data = await handler.buying(1, 5)
        assert result == "Purchase successful"
        assert all(key in data for key in ['market-item', 'inventory-item', 'bank-update'])
        handler.banking_crud.update_bank_balance.assert_awaited_once_with(1, 500)
        handler.banking_crud.update_bank_balance_by_username.assert_awaited_once_with("seller", 500)
        mock_session.add.assert_called_once()


    async def test_quick_sell(self, handler, mock_session, mock_inventory_item):
        mock_session.get = AsyncMock(return_value=mock_inventory_item)
        handler.banking_crud.get_user_bank_from_userid = AsyncMock(return_value=(1, 1000))
        mock_inventory_item.amount_in_stash = 10
        mock_inventory_item.quick_sell_value = 50
        result, data = await handler.quick_sell(1, 10)  # $50 * 10
        assert result == "Quick-Sell Successful"
        assert data['bank'] == 1500
        handler.banking_crud.update_bank_balance.assert_awaited_once_with(1, 1500)
        handler.inv_crud.update_any_inventory_quantity.assert_awaited_once_with(1, -10, mock_inventory_item)


    async def test_cancel_market_post(self, handler, mock_session, mock_market_item):
        mock_market_item.by_user = "testuser"
        handler.market_crud.get_market_item_from_market_id = AsyncMock(return_value=mock_market_item)
        handler.inv_crud.get_user_inventory_id_by_userid = AsyncMock(return_value=1)
        handler.inv_crud.get_inventory_item_by_item_id = AsyncMock(return_value=None)
        result, data = await handler.cancel_market_post(1)
        assert result == "Item taken off the market"
        assert all(key in data for key in ['market-item', 'inventory-item'])
        mock_session.add.assert_called_once()
        mock_session.delete.assert_called_once_with(mock_market_item)


    async def test_buying_less_stock(self, handler, mock_session, mock_market_item):
        mock_market_item.item_quantity = 5
        handler.market_crud.get_market_item_from_market_id = AsyncMock(return_value=mock_market_item)
        handler.banking_crud.get_user_bank_from_userid = AsyncMock(return_value=(1, 1000))
        handler.inv_crud.get_inventory_item_by_item_id = AsyncMock(return_value=None)
        result, data = await handler.buying(1, 10)
        assert result == "Purchase successful"
        assert data['inventory-item'].amount_in_stash == 5
        assert all(key in data for key in ['market-item', 'inventory-item', 'bank-update'])
        handler.banking_crud.update_bank_balance.assert_awaited_once_with(1, 500)
        handler.banking_crud.update_bank_balance_by_username.assert_awaited_once_with("seller", 500)
        mock_session.add.assert_called_once()


    async def test_market_transaction_invalid(self, handler):
        handler.transaction_data.transaction_type = "INVALID"
        with pytest.raises(ValueError, match="Invalid Transaction"):
            await handler.market_transaction()


    async def test_buying_own_item(self, handler, mock_market_item):
        mock_market_item.by_user = "testuser"
        handler.market_crud.get_market_item_from_market_id = AsyncMock(return_value=mock_market_item)
        with pytest.raises(ValueError, match="You can't buy your own items"):
            await handler.buying(1, 5)


    async def test_buying_insufficient_funds(self, handler, mock_market_item):
        handler.market_crud.get_market_item_from_market_id = AsyncMock(return_value=mock_market_item)
        handler.banking_crud.get_user_bank_from_userid = AsyncMock(return_value=(1, 100))
        with pytest.raises(ValueError, match="Not enough money to purchase that item"):
            await handler.buying(1, 5)


    async def test_quick_sell_insufficient_quantity(self, handler, mock_session, mock_inventory_item):
        mock_inventory_item.amount_in_stash = 3
        mock_session.get = AsyncMock(return_value=mock_inventory_item)
        with pytest.raises(ValueError, match="Invalid amount"):
            await handler.quick_sell(1, 5)


    async def test_cancel_market_post_not_owner(self, handler, mock_market_item):
        mock_market_item.by_user = "otheruser"
        handler.market_crud.get_market_item_from_market_id = AsyncMock(return_value=mock_market_item)
        with pytest.raises(ValueError, match="That's not your item"):
            await handler.cancel_market_post(1)


    async def test_buying_non_existent_item(self, handler):
        handler.market_crud.get_market_item_from_market_id = AsyncMock(return_value=None)
        with pytest.raises(LookupError, match="Market item not found"):
            await handler.buying(1, 5)


    async def test_quick_sell_non_existent_item(self, handler, mock_session):
        mock_session.get = AsyncMock(return_value=None)
        with pytest.raises(LookupError, match="Inventory item not found"):
            await handler.quick_sell(1, 5)


    async def test_cancel_non_existent_market_post(self, handler):
        handler.market_crud.get_market_item_from_market_id = AsyncMock(return_value=None)
        with pytest.raises(LookupError, match="Market item not found"):
            await handler.cancel_market_post(1)
