import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.game_systems.crews.crew_handler import CrewHandler
from app.models import Crew
from app.schemas import NewCrewInfo


@pytest.fixture
def handler(mock_crew_crud, mock_user_crud):
    mock_session = AsyncMock()
    handler = CrewHandler(mock_session)
    handler.crew_crud = mock_crew_crud
    handler.user_crud = mock_user_crud
    handler.user_crud.get_user_field_from_id = AsyncMock(return_value=None)
    handler.crew_crud.check_existing_crew_name = AsyncMock(return_value=None)
    return handler


class TestCrewHandler:

    async def test_before_create_checks_crew_name_taken(self, handler):
        handler.crew_crud.check_existing_crew_name = AsyncMock(return_value=True)
        with pytest.raises(ValueError, match="A crew with that name already exists."):
            await handler.before_create_checks("Taken Crew", 1)


    async def test_create_crew_success(self, handler):
        handler.session.add = Mock()
        new_crew_data = NewCrewInfo(name="Test Crew", private=False)
        new_crew = await handler.create_crew(new_crew_data, 1, "Test Leader")
        assert new_crew.name == "Test Crew"
        assert new_crew.leader == "Test Leader"
        handler.session.add.assert_called()


    async def test_create_crew_with_long_name(self, handler):
        new_crew_data = NewCrewInfo(name="A" * 300, private=False)
        with pytest.raises(ValueError, match="Crew name is too long"):
            await handler.create_crew(new_crew_data, 1, "Test Leader")


    async def test_create_crew_with_empty_name(self, handler):
        new_crew_data = NewCrewInfo(name="", private=False)
        with pytest.raises(ValueError, match="Crew name is too short"):
            await handler.create_crew(new_crew_data, 1, "Test Leader")


    async def test_add_user_to_crew(self, handler):
        handler.user_crud.get_user_field_from_username = AsyncMock(return_value=1)
        handler.user_crud.change_user_crew_id = AsyncMock(return_value=True)
        result = await handler.add_user_to_crew("TestUser", 1)
        assert result == "Successfully added to the crew"


    async def test_remove_user_from_crew(self, handler):
        handler.user_crud.get_user_field_from_username = AsyncMock(return_value=1)
        handler.user_crud.change_user_crew_id = AsyncMock()
        result = await handler.remove_player_from_crew("TestUser", 1)
        assert result == "Successfully removed the player from Crew"
        handler.user_crud.change_user_crew_id.assert_awaited_once_with("TestUser", crew_id=None)


    async def test_create_crew_for_different_users(self, handler):
        handler.session.add = Mock()
        for i in range(10):
            new_crew_data = NewCrewInfo(name=f"Test Crew {i}", private=False)
            user_id = i + 1
            new_crew = await handler.create_crew(new_crew_data, user_id, f"Leader {i}")
            assert new_crew.name == f"Test Crew {i}"
            assert new_crew.leader == f"Leader {i}"
            handler.session.add.assert_called()
