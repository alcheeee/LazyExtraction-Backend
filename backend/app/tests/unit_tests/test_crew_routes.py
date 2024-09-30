import pytest
import inspect
from fastapi import HTTPException
from unittest.mock import AsyncMock, MagicMock, patch
from app.schemas import NewCrewInfo, AddRemoveCrewRequest
from app.game_systems.crews.crew_handler import CrewHandler
from app.routes import crew_routes


@pytest.fixture(autouse=True)
def unwrap_routes(monkeypatch):
    for name, func in inspect.getmembers(crew_routes, inspect.iscoroutinefunction):
        if hasattr(func, '__wrapped__'):
            monkeypatch.setattr(crew_routes, name, func.__wrapped__)


@pytest.fixture
def mock_crew_dependencies(monkeypatch):
    mock_crew_handler = AsyncMock()
    monkeypatch.setattr("app.routes.crew_routes.CrewHandler", MagicMock(return_value=mock_crew_handler))
    return mock_crew_handler


@pytest.fixture
def mock_exception_decorator():
    def mock_decorator(func):
        return func
    with patch('app.routes.crew_routes.exception_decorator', mock_decorator):
        yield


@pytest.fixture
def mock_user_data():
    return {
        'user': {
            'username': 'testuser',
            'user_id': '1'
        }
    }


async def test_create_crew_success(mock_crew_dependencies, mock_session, mock_user_data):
    request = NewCrewInfo(name="Test Crew", description="A test crew")
    mock_crew_dependencies.create_crew.return_value = MagicMock(id=1)  # noqa
    result = await crew_routes.create_crew(request, mock_session, mock_user_data)
    assert "Test Crew created successfully!" in result['message']
    mock_crew_dependencies.create_crew.assert_called_once_with(request, 1, 'testuser')  # noqa
    mock_crew_dependencies.add_user_to_crew.assert_called_once_with('testuser', 1)  # noqa
    mock_session.commit.assert_called()


async def test_add_user_to_crew_success(mock_crew_dependencies, mock_session, mock_user_data):
    request = AddRemoveCrewRequest(crew_id=1, user_to_add_remove="newuser")
    mock_crew_dependencies.crew_leader_check.return_value = 'testuser'
    mock_crew_dependencies.add_user_to_crew.return_value = "User added successfully"  # noqa
    result = await crew_routes.add_user_to_crew(request, mock_user_data, mock_session)
    assert "User added successfully" in result['message']
    mock_crew_dependencies.crew_leader_check.assert_called_once_with('testuser', 1)
    mock_crew_dependencies.add_user_to_crew.assert_called_once_with("newuser", 1)  # noqa
    mock_session.commit.assert_called_once()


async def test_add_user_to_crew_leader_error(mock_crew_dependencies, mock_session, mock_user_data):
    request = AddRemoveCrewRequest(crew_id=1, user_to_add_remove="testuser")
    mock_crew_dependencies.crew_leader_check.return_value = 'testuser'
    with pytest.raises(ValueError, match="You can't add yourself!"):
        await crew_routes.add_user_to_crew(request, mock_user_data, mock_session)


async def test_remove_user_from_crew_success(mock_crew_dependencies, mock_session, mock_user_data):
    request = AddRemoveCrewRequest(crew_id=1, user_to_add_remove="usertoremove")
    mock_crew_dependencies.crew_leader_check.return_value = 'testuser'
    mock_crew_dependencies.remove_player_from_crew.return_value = "User removed successfully"
    result = await crew_routes.remove_user_from_crew(request, mock_user_data, mock_session)
    assert "User removed successfully" in result['message']
    mock_crew_dependencies.crew_leader_check.assert_called_once_with('testuser', 1)
    mock_crew_dependencies.remove_player_from_crew.assert_called_once_with("usertoremove", 1)
    mock_session.commit.assert_called_once()


async def test_remove_user_from_crew_leader_error(mock_crew_dependencies, mock_session, mock_user_data):
    request = AddRemoveCrewRequest(crew_id=1, user_to_add_remove="testuser")
    mock_crew_dependencies.crew_leader_check.return_value = 'testuser'
    with pytest.raises(ValueError, match="Cannot remove yourself, disband the Crew first"):
        await crew_routes.remove_user_from_crew(request, mock_user_data, mock_session)


