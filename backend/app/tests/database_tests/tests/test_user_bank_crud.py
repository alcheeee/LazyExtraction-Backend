import pytest
from app.crud.user_bank_crud import UserBankingCRUD
from app.models import User, Inventory


async def test_get_user_bank_from_userid(test_session, db_user):
    """Test retrieving the bank balance and inventory id for a user"""
    user = db_user
    banking_crud = UserBankingCRUD(test_session)
    inventory_details = await banking_crud.get_user_bank_from_userid(user.id)
    assert inventory_details is not None
    inventory_id, bank_balance = inventory_details
    assert bank_balance == 1000
    assert inventory_id == user.inventory.id


async def test_update_bank_balance(test_session, db_user):
    """Test updating the bank balance for a specific inventory id"""
    user = db_user
    banking_crud = UserBankingCRUD(test_session)
    new_balance = 5000
    await banking_crud.update_bank_balance(user.inventory.id, new_balance)
    updated_inventory = await test_session.get(Inventory, user.inventory.id)
    assert updated_inventory.bank == new_balance


async def test_update_bank_balance_by_username(test_session, db_user):
    """Test updating the bank balance for a user by username"""
    user = db_user
    banking_crud = UserBankingCRUD(test_session)
    balance_adjustment = 2500
    new_balance = await banking_crud.update_bank_balance_by_username(user.username, balance_adjustment)
    updated_inventory = await test_session.get(Inventory, user.inventory.id)
    assert updated_inventory.bank == 1000 + balance_adjustment
    assert new_balance == 1000 + balance_adjustment


async def test_update_bank_balance_negative(test_session, db_user):
    """Test that the bank balance can be reduced by a specific amount"""
    user = db_user
    banking_crud = UserBankingCRUD(test_session)
    balance_adjustment = -500
    new_balance = await banking_crud.update_bank_balance_by_username(user.username, balance_adjustment)
    updated_inventory = await test_session.get(Inventory, user.inventory.id)
    assert updated_inventory.bank == 1000 + balance_adjustment
    assert new_balance == 1000 + balance_adjustment


async def test_get_user_bank_invalid_user(test_session):
    """Test handling of invalid user id when retrieving bank balance"""
    banking_crud = UserBankingCRUD(test_session)
    with pytest.raises(LookupError, match="Failed to get user Inventory or Bank"):
        await banking_crud.get_user_bank_from_userid(9999)


async def test_update_bank_balance_invalid_username(test_session):
    """Test handling of invalid username when updating bank balance"""
    banking_crud = UserBankingCRUD(test_session)
    with pytest.raises(LookupError, match="Failed to get user Inventory or Bank"):
        await banking_crud.update_bank_balance_by_username("invalid_username", 1000)

