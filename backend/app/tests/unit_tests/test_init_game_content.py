import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.database.init_db import init_content, InitializeLazyBot
from app.models.models import User


ItemsCRUD = 'app.database.init_db.ItemsCRUD'
UserHandler = 'app.database.init_db.UserHandler'
UserCRUD = 'app.database.init_db.UserCRUD'


class TestInitGameContent:

    @patch(ItemsCRUD)
    async def test_init_content(self, mock_items_crud):
        mock_session = AsyncMock()
        mock_session.add = Mock()
        mock_items_crud.return_value.check_item_exists = AsyncMock(return_value=None)
        result = await init_content(mock_session)
        mock_session.commit.assert_awaited_once()
        mock_session.add.assert_called()
        assert mock_session.add.call_count > 0
        assert result is True


class TestInitializeLazyBot:

    @patch(UserHandler)
    @patch(UserCRUD)
    async def test_check_bot_account_exists(self, mock_user_crud, mock_user_handler):
        mock_session = AsyncMock()
        mock_user_crud.return_value.get_user_field_from_username = AsyncMock(return_value=1)
        bot_initializer = InitializeLazyBot(mock_session)
        await bot_initializer.check_bot_account()
        assert bot_initializer.bot_id == 1
        mock_user_handler.create_user.assert_not_called()


    @patch('app.database.init_db.InitializeLazyBot.init_bot_inventory', new_callable=AsyncMock)
    @patch('app.database.init_db.InitializeLazyBot.make_bot_admin', new_callable=AsyncMock)
    @patch(UserHandler)
    @patch(UserCRUD)
    async def test_create_bot_account(
            self, mock_user_crud, mock_user_handler, mock_make_bot_admin, mock_init_bot_inventory
    ):
        mock_session = AsyncMock()
        mock_user_handler.return_value.create_user = AsyncMock(return_value=AsyncMock(id=1))
        mock_user_crud.return_value.make_bot_admin = AsyncMock(return_value=True)
        bot_initializer = InitializeLazyBot(mock_session)
        await bot_initializer.create_bot_account()
        mock_user_handler.return_value.create_user.assert_awaited_once()
        assert bot_initializer.bot_id == 1
        mock_make_bot_admin.assert_awaited_once()
        mock_init_bot_inventory.assert_awaited_once()


    @patch(UserCRUD)
    async def test_make_bot_admin(self, mock_user_crud):
        mock_session = AsyncMock()
        mock_user_crud.return_value.make_user_admin = AsyncMock(return_value=True)
        bot_initializer = InitializeLazyBot(mock_session)
        bot_initializer.bot_id = 1
        await bot_initializer.make_bot_admin()
        mock_user_crud.return_value.make_user_admin.assert_awaited_once_with(1)


    @patch(ItemsCRUD)
    @patch('app.database.init_db.UserInventoryCRUD')
    async def test_add_item_to_inventory(self, mock_user_inv_crud, mock_items_crud):
        mock_session = AsyncMock()
        mock_items_crud.return_value.check_item_exists = AsyncMock(return_value=1)
        mock_user_inv_crud.return_value.update_user_inventory_item = AsyncMock(return_value=AsyncMock(id=3))
        bot_initializer = InitializeLazyBot(mock_session)
        bot_initializer.bot_id = 1
        new_item = await bot_initializer.add_item_to_inventory("M4A1 Carbine")
        mock_items_crud.return_value.check_item_exists.assert_awaited_once_with("M4A1 Carbine")
        mock_user_inv_crud.return_value.update_user_inventory_item.assert_awaited_once()
        assert new_item.id == 3


    @patch('app.database.init_db.ItemStatsHandler')
    async def test_handle_equipment(self, mock_item_stats_handler):
        mock_session = AsyncMock()
        mock_item_stats_handler.return_value.equip_item = AsyncMock(return_value=True)
        new_item = AsyncMock(id=1, item_name="M4A1 Carbine")
        bot_initializer = InitializeLazyBot(mock_session)
        bot_initializer.bot_id = 1
        await bot_initializer.handle_equipment(new_item, ['Tactical Laser', 'Flash Suppressor'])
        mock_item_stats_handler.return_value.equip_item.assert_awaited_once()
