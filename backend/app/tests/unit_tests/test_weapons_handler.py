import pytest
from unittest.mock import AsyncMock, Mock, patch

from app.game_systems.items.weapons.attachment_handler import WeaponAttachmentsHandler
from app.crud import UserInventoryCRUD, ItemsCRUD, WeaponCRUD

from app.models import InventoryItem, Items, Weapon, Attachments


@pytest.fixture
def mock_weapon_details():
    weapon_details = Mock()
    weapon_details.damage = 10
    weapon_details.strength_adj = 2
    weapon_details.agility_adj = 1
    return weapon_details


@pytest.fixture
def handler(mock_inventory, mock_items_crud, mock_inventory_item, mock_item, mock_weapon_details):
    handler = WeaponAttachmentsHandler(session=AsyncMock(), user_id=1, weapon_inventory_id=1)
    handler.weapon_crud.get_user_weapon = AsyncMock(return_value=(
        mock_item, mock_inventory_item)
    )
    return handler


# TODO : Add tests
