import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.models.models import (
    User,
    Stats,
    Inventory,
    InventoryItem
)
from app.models.item_models import (
    Items,
    Clothing,
    Armor
)
from app.models.weapon_models import Weapon
from app.schemas import (
    ItemType,
    ClothingType,
    ArmorType
)


@pytest.fixture
def mock_session():
    mock_session = AsyncMock()
    mock_session.add_all = Mock()
    mock_session.add = Mock()
    return mock_session


@pytest.fixture
def mock_crew_crud():
    with patch('app.crud.crew_crud.CrewCRUD') as mock:
        yield mock.return_value

@pytest.fixture
def mock_user_crud():
    with patch('app.crud.user_crud.UserCRUD') as mock:
        yield mock.return_value

@pytest.fixture
def mock_items_crud():
    with patch('app.crud.items_crud.ItemsCRUD') as mock:
        yield mock.return_value

@pytest.fixture
def mock_user_inv_crud():
    with patch('app.crud.user_inv_crud.UserInventoryCRUD') as mock:
        yield mock.return_value


@pytest.fixture
def mock_user():
    """Fixture to mock a user."""
    user = AsyncMock(spec=User)
    user.id = 1
    user.stats_id = 1
    user.inventory_id = 1
    user.stats = Mock()
    user.stats.round_stats = AsyncMock()
    user.in_raid = False
    user.current_room_data = None
    user.current_world = None
    user.actions_left = 0
    user.stats.knowledge = 1.0
    user.stats.level = 1.0
    user.stats.reputation = 10
    user.stats.max_energy = 100
    user.stats.strength = 1
    user.stats.agility = 1
    return user


@pytest.fixture
def mock_stats():
    stats = AsyncMock(spec=Stats)
    stats.reputation = 10
    stats.max_energy = 100
    stats.strength = 1
    stats.agility = 1
    stats.round_stats = AsyncMock()
    return stats


@pytest.fixture
def mock_inventory():
    inventory = Mock(spec=Inventory)
    inventory.equipped_weapon_id = None
    inventory.equipped_mask_id = None
    inventory.equipped_body_id = None
    inventory.equipped_legs_id = None
    inventory.equipped_body_armor_id = None
    inventory.equipped_head_armor_id = None
    return inventory


@pytest.fixture
def mock_inventory_item():
    inventory_item = Mock(spec=InventoryItem)
    inventory_item.id = 1
    inventory_item.item_name = "Test Item"
    inventory_item.amount_in_inventory = 1
    inventory_item.amount_in_stash = 0
    inventory_item.item_id = 1
    inventory_item.one_equipped = False
    inventory_item.quick_sell_value = 0
    inventory_item.is_modified = False
    inventory_item.modifications = None
    return inventory_item


@pytest.fixture
def mock_item():
    item = Mock(spec=Items)
    item.weight = 1.0
    item.category = ItemType.Weapon
    return item

