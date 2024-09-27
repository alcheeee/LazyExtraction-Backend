import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.models import User, Stats

from app.game_systems.game_world.room_generator import RoomGenerator
from app.schemas.world_schemas import WorldNames


@pytest.fixture
def mock_room_data():
    """Mock data for room generation."""
    return {
        'potential_rooms': [
            ['medical_room', 25],
            ['regular_room', 75]
        ]
    }


@pytest.fixture
def mock_get_user(mock_user):
    with patch('app.game_systems.game_world.room_generator.UserCRUD.get_user_for_interaction') as mock:
        yield mock


class TestRoomGenerator:

    @pytest.fixture(autouse=True)
    def setup(self, mock_room_data):
        """Set up RoomGenerator with mock data."""
        with patch('app.game_systems.game_world.room_generator.room_tables', {WorldNames.Forest: mock_room_data}):
            self.room_gen = RoomGenerator(WorldNames.Forest)
            self.room_gen.loot_generator = AsyncMock()


    def test__get_room_types_and_weights(self):
        """Test if room types and weights are correctly retrieved."""
        room_types, room_weights = self.room_gen._get_room_types_and_weights()
        assert 'medical_room' in room_types
        assert 'regular_room' in room_types
        assert room_weights == (25, 75)


    def test__choose_room_type(self):
        """Test if the correct room type is chosen based on weights."""
        with patch('random.choices', return_value=['medical_room']):
            room_type = self.room_gen._choose_room_type()
            assert room_type == 'medical_room'


    async def test_generate_room(self):
        """Test async room generation."""
        self.room_gen.loot_generator.pick_drops.return_value = ['item1', 'item2']
        room = await self.room_gen.generate_room()
        assert room['room_type'] in ('regular_room', 'medical_room', 'military_room')
        assert room['items'] == [{'id': 0, 'name': 'item1'}, {'id': 1, 'name': 'item2'}]
        assert len(room['connections']) >= 1
        assert len(room['connections']) <= 3


    async def test_assign_room_to_user(self, mock_user, mock_get_user, mock_session):
        """Test the `assign_room_to_user` method."""
        mock_get_user.return_value = mock_user
        with patch.object(
                self.room_gen, 'generate_room',
                return_value={"room_type": "regular_room", "items": [], "connections": [1, 2]}
        ):
            room_data = await self.room_gen.assign_room_to_user(mock_user.id, mock_session)
            assert room_data["room_type"] == "regular_room"
            assert mock_user.current_room_data == room_data
            assert mock_user.current_world == WorldNames.Forest
            assert mock_user.actions_left == 20
            assert mock_user.in_raid is True
            assert mock_user.stats.level == 1.1
            assert mock_user.stats.knowledge == 1.1
            mock_user.stats.round_stats.assert_called_once()


    async def test_assign_room_user_already_in_raid(self, mock_get_user, mock_user):
        """Test `assign_room_to_user` when the user is already in a raid."""
        mock_session = AsyncMock()
        mock_user.in_raid = True
        mock_get_user.return_value = mock_user
        with pytest.raises(ValueError, match="Already in a raid"):
            await self.room_gen.assign_room_to_user(mock_user.id, mock_session)
