import pytest
from app.crud.user_crud import UserCRUD
from app.models import User, Inventory, Stats


async def test_make_user_admin(test_session, db_user):
    """Test making a user an admin"""
    user = db_user
    user_crud = UserCRUD(User, test_session)
    result = await user_crud.make_user_admin(user.id)
    assert result is True
    updated_user = await test_session.get(User, user.id)
    assert updated_user.is_admin is True


async def test_get_user_field_from_id(test_session, db_user):
    """Test retrieving a user field by ID"""
    user = db_user
    user_crud = UserCRUD(User, test_session)
    email = await user_crud.get_user_field_from_id(user.id, "email")
    assert email == user.email


async def test_get_user_field_from_username(test_session, db_user):
    """Test retrieving a user field by username"""
    user = db_user
    user_crud = UserCRUD(User, test_session)
    email = await user_crud.get_user_field_from_username(user.username, "email")
    assert email == user.email


async def test_get_user_for_interaction(test_session, db_user):
    """Test retrieving a user for interaction"""
    user = db_user
    user_crud = UserCRUD(User, test_session)
    user_interaction = await user_crud.get_user_for_interaction(user.id)
    assert user_interaction is not None
    assert user_interaction.id == user.id
    assert user_interaction.stats is not None  # Ensure the related stats are preloaded


async def test_change_user_crew_id(test_session, temp_user):
    from app.tests.database_tests.model_factories import CrewFactory
    """Test changing a user's crew ID"""
    test_crew = CrewFactory()
    user = temp_user()
    test_session.add_all([test_crew, user])
    await test_session.commit()
    user_crud = UserCRUD(User, test_session)
    result = await user_crud.change_user_crew_id(user.username, crew_id=test_crew.id)
    assert result is True
    updated_user = await test_session.get(User, user.id)
    assert updated_user.crew_id == test_crew.id


async def test_is_user_admin(test_session, db_user):
    """Test checking if a user is an admin"""
    user = db_user
    user_crud = UserCRUD(User, test_session)
    is_admin = await user_crud.is_user_admin(user.id)
    assert is_admin is False
    await user_crud.make_user_admin(user.id)
    is_admin = await user_crud.is_user_admin(user.id)
    assert is_admin == user.username


async def test_get_stats_inv_ids_and_jobname(test_session, db_user):
    """Test retrieving user stats, inventory IDs, and job name"""
    user = db_user
    user_crud = UserCRUD(User, test_session)
    stats_id, inventory_id, job = await user_crud.get_stats_inv_ids_and_jobname(user.id)
    assert stats_id == user.stats_id
    assert inventory_id == user.inventory_id
    assert job == user.job


async def test_get_stats_education(test_session, db_user):
    """Test retrieving user stats and training progress"""
    user = db_user
    user_crud = UserCRUD(User, test_session)
    returned_user = await user_crud.get_stats_training(user.id)
    assert returned_user is not None
    assert returned_user.id == user.id
    assert returned_user.stats is not None
    assert returned_user.training_progress is not None
    assert returned_user.training_progress.basic_training == 0.0
