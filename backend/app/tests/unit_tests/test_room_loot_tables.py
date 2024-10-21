import pytest
from unittest.mock import patch
from app.game_systems.game_world.room_loot_handler import RoomLootTables
from app.schemas.world_schemas import WorldNames


@pytest.fixture
def mock_drops():
    """Mock data for room drops."""
    return {
        'regular_room_drops': {
            WorldNames.Forest: {'item1': 1, 'item2': 2},
        },
        'medical_room_drops': {
            WorldNames.Forest: {'med_kit': 1, 'bandage': 3},
        },
        'military_room_drops': {
            WorldNames.Forest: {'ammo': 5, 'rifle': 1},
        }
    }


@pytest.fixture
def mock_random():
    with patch('random.choices') as mock:
        yield mock


class TestRoomLootTables:
    @pytest.fixture(autouse=True)
    def setup(self, mock_drops):
        """Set up RoomLootTables with mock data."""
        with patch('app.game_systems.game_world.room_loot_handler.room_loot_tables', mock_drops):
            self.loot_tables = RoomLootTables(WorldNames.Forest)

    def test_prepare_drops(self):
        """Test if drops are correctly prepared for a room type."""
        items, weights = self.loot_tables._prepare_drops('regular_room')
        assert list(items) == ['item1', 'item2']
        assert list(weights) == [1, 2]

    async def test_pick_drops(self, mock_random):
        """Test if the correct number of items is picked based on drop ranges."""
        mock_random.return_value = ['item1']
        items = await self.loot_tables.pick_drops('regular_room')
        assert items == ['item1']

    async def test_pick_drops_range(self):
        """Test if the number of items dropped is within the specified range."""
        with patch('random.randint', return_value=2):
            items = await self.loot_tables.pick_drops('regular_room')
            assert len(items) == 2

    async def test_regular_room_drops(self, mock_random):
        """Test specific room loot generation."""
        mock_random.return_value = ['item1']
        items = await self.loot_tables.pick_drops('regular_room')
        assert items == ['item1']

    async def test_medical_room_drops(self, mock_random):
        """Test medical room loot generation."""
        mock_random.return_value = ['med_kit']
        items = await self.loot_tables.pick_drops('medical_room')
        assert items == ['med_kit']

    async def test_military_room_drops(self, mock_random):
        """Test military room loot generation."""
        mock_random.return_value = ['ammo']
        items = await self.loot_tables.pick_drops('military_room')
        assert items == ['ammo']
