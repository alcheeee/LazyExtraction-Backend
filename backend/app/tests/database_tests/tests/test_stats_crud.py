import pytest
import factory
from faker import Faker
from app.crud.stats_crud import StatsCRUD
from app.models import User, Inventory, Stats


async def test_adjust_user_weight(test_session, db_user):
    """Test adjusting user weight"""
    user = db_user
    user.inventory.current_weight = 50.0
    stats_crud = StatsCRUD(test_session)
    new_weight = await stats_crud.adjust_user_weight(user.id, 10.5)
    assert new_weight == 60.5
    updated_inventory = await test_session.get(Inventory, user.inventory.id)
    assert updated_inventory.current_weight == 60.5


async def test_weight_below_zero(test_session, db_user):
    user = db_user
    stats_crud = StatsCRUD(test_session)
    new_weight = await stats_crud.adjust_user_weight(user.id, -100.0)
    assert new_weight == 0.0
    updated_inventory = await test_session.get(Inventory, user.inventory.id)
    assert updated_inventory.current_weight == 0.0


async def test_adjust_multiple_stats(test_session, db_user):
    """Test adjusting multiple user stats"""
    user = db_user
    stats_crud = StatsCRUD(test_session)
    stat_adjustments = {"level": 2.0, "strength": 5.0, "luck": -1.0}
    updated_stats = await stats_crud.adjust_user_stats(user.id, stat_adjustments)
    assert updated_stats.level == 3.0
    assert updated_stats.strength == 6.0
    assert updated_stats.luck == 0.0


async def test_invalid_stat_name(test_session, db_user):
    """Test handling invalid stat name adjustment"""
    user = db_user
    stats_crud = StatsCRUD(test_session)
    stat_adjustments = {
        "invalid_stat": 10
    }
    with pytest.raises(ValueError, match="Invalid stat name: invalid_stat"):
        await stats_crud.adjust_user_stats(user.id, stat_adjustments)


async def test_adjust_stats_for_nonexistent_user(test_session):
    """Test adjusting stats for a user that doesn't exist"""
    stats_crud = StatsCRUD(test_session)
    stat_adjustments = {
        "level": 2.0
    }
    with pytest.raises(LookupError, match="Stats not found for user_id: 9999"):
        await stats_crud.adjust_user_stats(9999, stat_adjustments)


async def test_adjust_weight_for_nonexistent_user(test_session):
    """Test adjusting weight for a non-existent user"""
    stats_crud = StatsCRUD(test_session)
    with pytest.raises(LookupError, match="No inventory found for user"):
        await stats_crud.adjust_user_weight(9999, 10.0)


async def test_adjust_weight_to_zero(test_session, db_user):
    """Test adjusting weight to ensure it doesn't go below zero"""
    user = db_user
    stats_crud = StatsCRUD(test_session)
    new_weight = await stats_crud.adjust_user_weight(user.id, -100.0)
    assert new_weight == 0.0
    updated_inventory = await test_session.get(Inventory, user.inventory.id)
    assert updated_inventory.current_weight == 0.0
