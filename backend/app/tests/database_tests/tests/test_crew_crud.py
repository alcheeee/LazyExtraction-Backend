import pytest
import factory
from app.crud.crew_crud import CrewCRUD
from app.models import Crew, User, CrewItems
from app.tests.database_tests.model_factories import CrewFactory


async def test_get_crew_by_id(test_session):
    """Test retrieving a Crew by its ID."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_session.add(test_crew)
    await test_session.commit()
    crew = await crew_crud.get_crew_by_id(test_crew.id)
    assert crew.id == test_crew.id
    assert crew.name == test_crew.name
    assert crew.leader == test_crew.leader


async def test_get_crew_name_by_id(test_session):
    """Test retrieving a Crew name by its ID."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_session.add(test_crew)
    await test_session.commit()
    crew_name = await crew_crud.get_crew_name_by_id(test_crew.id)
    assert crew_name == test_crew.name


async def test_check_existing_crew_name(test_session):
    """Test checking if a Crew name already exists."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_session.add(test_crew)
    await test_session.commit()
    result = await crew_crud.check_existing_crew_name(test_crew.name)
    assert result is not None
    assert result == test_crew.name


async def test_get_crew_leader(test_session):
    """Test getting the leader of a Crew by ID."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_session.add(test_crew)
    await test_session.commit()
    leader = await crew_crud.get_crew_leader(test_crew.id)
    assert leader == test_crew.leader


async def test_delete_crew(test_session):
    """Test deleting a Crew by ID."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_session.add(test_crew)
    await test_session.commit()
    await crew_crud.delete_crew(test_crew.id)
    crew = await crew_crud.get_crew_by_id(test_crew.id)
    assert crew is None


async def test_remove_all_users_from_crew(test_session, temp_user):
    """Test removing all users from a Crew."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_user = temp_user()
    test_session.add(test_crew)
    test_session.add(test_user)
    await test_session.commit()
    await crew_crud.remove_all_users_from_crew(test_crew.id)
    user = await test_session.get(User, test_user.id)
    assert user.crew_id is None


async def test_get_all_crew_members(test_session, temp_user):
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_user1 = temp_user()
    test_user2 = temp_user()
    test_user1.crew_id = test_crew.id
    test_user2.crew_id = test_crew.id
    test_session.add(test_crew)
    test_session.add(test_user1)
    test_session.add(test_user2)
    await test_session.commit()
    members = await crew_crud.get_all_crew_members(test_crew.id)
    assert len(members) == 2
    assert test_user1.id in members
    assert test_user2.id in members


async def test_delete_crew_items(test_session):
    """Test removing all items linked to a crew."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_item = CrewItems(item_name="Components", quantity=1, crew_id=test_crew.id)
    test_session.add(test_crew)
    test_session.add(test_item)
    await test_session.commit()
    await crew_crud.delete_crew_items(test_crew.id)
    item = await test_session.get(CrewItems, test_item.id)
    assert item is None


async def test_add_item_to_crew(test_session):
    """Test adding an item to a Crew."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_session.add(test_crew)
    await test_session.commit()
    item_data = {"item_name": "Crew Item", "quantity": 1}
    new_item = await crew_crud.add_item_to_crew(test_crew.id, item_data)
    assert new_item.item_name == "Crew Item"
    assert new_item.crew_id == test_crew.id


async def test_get_non_existent_crew_by_id(test_session):
    """Test retrieving a non-existent Crew by its ID."""
    crew_crud = CrewCRUD(Crew, test_session)
    crew = await crew_crud.get_crew_by_id(999)
    assert crew is None


async def test_get_crew_name_by_non_existent_id(test_session):
    """Test retrieving a Crew name by a non-existent ID."""
    crew_crud = CrewCRUD(Crew, test_session)
    crew_name = await crew_crud.get_crew_name_by_id(999)
    assert crew_name is None


async def test_check_non_existing_crew_name(test_session):
    """Test checking if a Crew name doesn't exist."""
    crew_crud = CrewCRUD(Crew, test_session)
    result = await crew_crud.check_existing_crew_name("NonExistentCrew")
    assert result is None


async def test_get_all_crew_members_no_members(test_session):
    """Test retrieving all members of a Crew with no members."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_session.add(test_crew)
    await test_session.commit()
    members = await crew_crud.get_all_crew_members(test_crew.id)
    assert len(members) == 0


async def test_remove_all_users_from_empty_crew(test_session):
    """Test removing all users from an empty Crew."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_session.add(test_crew)
    await test_session.commit()
    await crew_crud.remove_all_users_from_crew(test_crew.id)
    members = await crew_crud.get_all_crew_members(test_crew.id)
    assert len(members) == 0


async def test_delete_crew_with_items(test_session):
    """Test deleting a Crew that has items associated with it."""
    crew_crud = CrewCRUD(Crew, test_session)
    test_crew = CrewFactory()
    test_item = CrewItems(item_name="Crew Item", quantity=10, crew_id=test_crew.id)
    test_session.add(test_crew)
    test_session.add(test_item)
    await test_session.commit()
    await crew_crud.delete_crew(test_crew.id)
    crew = await crew_crud.get_crew_by_id(test_crew.id)
    assert crew is None
    item = await test_session.get(CrewItems, test_item.id)
    assert item is None


async def test_delete_non_existent_crew(test_session):
    """Test deleting a non-existent Crew."""
    crew_crud = CrewCRUD(Crew, test_session)
    with pytest.raises(LookupError):
        await crew_crud.delete_crew(999)

