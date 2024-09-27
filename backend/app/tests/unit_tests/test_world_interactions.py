import pytest
from pydantic import ValidationError
from unittest.mock import AsyncMock, Mock, patch
from app.game_systems.game_world.world_interactions import InteractionHandler
from app.schemas import RoomInteraction, InteractionTypes


@pytest.fixture
def mock_interaction(mock_items_crud, mock_user_inv_crud, mock_user):
    interaction = InteractionHandler(AsyncMock(), 1)
    interaction.item_crud = mock_items_crud
    interaction.user_inv_crud = mock_user_inv_crud
    mock_user.current_room_data = {
        "room_type": "regular_room",
        "items": [
            {"id": 1, "name": "item1"},
            {"id": 2, "name": "item2"}
        ],
        "connections": [3, 4]
    }
    return interaction


async def test_item_pickup_success(mock_interaction, mock_items_crud, mock_user_inv_crud, mock_user):
    """Test successful item pickup."""
    mock_items_crud.check_item_exists = AsyncMock(return_value=1001)
    mock_user_inv_crud.update_user_inventory_item = AsyncMock(return_value="inventory_item_mock")
    mock_user.actions_left = 5

    with patch('app.game_systems.game_world.world_interactions.flag_modified') as mock_flag_modified:
        result = await mock_interaction.item_pickup(mock_user, 1)
        assert result[0] == "You picked up item1"
        assert mock_user.actions_left == 4
        assert "picked-up" in result[1]
        assert result[1]["picked-up"]["name"] == "item1"
        mock_flag_modified.assert_called_once_with(mock_user, "current_room_data")
        mock_user_inv_crud.update_user_inventory_item.assert_awaited_once_with(
            mock_user.inventory_id, 1001, 1, to_stash=False
        )


async def test_item_pickup_not_in_room(mock_interaction, mock_user):
    """Test item not in room during pickup."""
    with pytest.raises(ValueError, match="Item not in room"):
        await mock_interaction.item_pickup(mock_user, 999)


async def test_item_pickup_no_db_reference(mock_interaction, mock_items_crud, mock_user):
    """Test item with no reference in database."""
    mock_items_crud.check_item_exists = AsyncMock(return_value=None)
    with pytest.raises(ValueError, match="Couldn't find a reference to that item"):
        await mock_interaction.item_pickup(mock_user, 1)


@patch('app.game_systems.game_world.world_interactions.RoomGenerator')
async def test_traverse_room_success(mock_room_generator, mock_interaction, mock_user):
    """Test successful room traversal."""
    mock_room_generator.return_value.generate_room = AsyncMock(return_value={
                "room_type": "new_room", "connections": [5, 6]
    })
    mock_user.actions_left = 5
    result = await mock_interaction.traverse_room(mock_user, 3)
    assert result[0] == "Entered a new room"
    assert mock_user.actions_left == 4
    assert "skill-adjustments" in result[1]


async def test_traverse_room_not_connected(mock_interaction, mock_user):
    """Test traversing to an unconnected room."""
    with pytest.raises(ValueError, match="New room is not connected to the current room"):
        await mock_interaction.traverse_room(mock_user, 999)


async def test_extract_from_raid_success(mock_interaction, mock_user):
    """Test successful extraction from raid."""
    mock_user.actions_left = 0
    result = await mock_interaction.extract_from_raid(mock_user)
    assert result[0] == "Successfully Extracted!"
    assert mock_user.in_raid is False
    assert mock_user.actions_left is None
    assert mock_user.current_world is None


async def test_extract_with_actions_left(mock_interaction, mock_user):
    """Test extraction attempt when actions are still remaining."""
    mock_user.actions_left = 5
    with pytest.raises(ValueError, match="You still need to perform 5 actions"):
        await mock_interaction.extract_from_raid(mock_user)


@patch('app.game_systems.game_world.world_interactions.RoomGenerator')
async def test_traverse_room_skill_adjustment(
        mock_room_generator, mock_user
):
    """Test skill adjustments during room traversal."""
    mock_room_generator.return_value.generate_room = AsyncMock(return_value={
        "room_type": "room", "connections": [5, 6]
    })
    mock_interaction = InteractionHandler(AsyncMock(), 1)
    mock_user.current_room_data = {
        "room_type": "regular_room",
        "items": [
            {"id": 1, "name": "item1"},
            {"id": 2, "name": "item2"}
        ],
        "connections": [3, 4]
    }
    result = await mock_interaction.traverse_room(mock_user, 3)
    assert "skill-adjustments" in result[1]
    assert result[1]["skill-adjustments"]["knowledge-adjustment"] == 0.1
    assert result[1]["skill-adjustments"]["level-adjustment"] == 0.1
    assert mock_user.stats.level == 1.1
    assert mock_user.stats.knowledge == 1.1


async def test_handle_invalid_action(mock_interaction, mock_user):
    """Test handle method with an invalid action."""
    with pytest.raises(ValidationError):
        interaction = RoomInteraction(action="INVALID_ACTION", id=1)
        await mock_interaction.handle(interaction)


async def test_handle_no_user_data(mock_interaction):
    """Test handle method when user data is not found."""
    interaction = RoomInteraction(action=InteractionTypes.Pickup, id=1)
    mock_interaction.user_crud.get_user_for_interaction = AsyncMock(return_value=None)
    with pytest.raises(LookupError, match="User data not found"):
        await mock_interaction.handle(interaction)
