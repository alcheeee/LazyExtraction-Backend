import pytest
from app.crud.user_inv_crud import UserInventoryCRUD
from app.models import InventoryItem, Items, Inventory, User
from app.tests.database_tests.model_factories import (
    InventoryItemFactory,
    ItemsFactory,
    UserFactory
)


async def test_get_inventory_item_by_userid(test_session, db_user, db_inventory_item):
    """Test retrieving inventory item by user id and item id."""
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=0, amount_in_stash=0)
    fetched_item = await user_inv_crud.get_inventory_item_by_userid(db_user.id, inventory_item.id)
    assert fetched_item.id == inventory_item.id
    assert fetched_item.item_name == inventory_item.item_name


async def test_switch_item_stash_status(test_session, db_user, db_inventory_item):
    """Test switching item stash status."""
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=10, amount_in_stash=0)
    original_db_item = inventory_item.copy()
    updated_item = await user_inv_crud.switch_item_stash_status(
        db_user.id, inventory_item.id, to_stash=True, quantity=5
    )
    assert updated_item.amount_in_inventory == original_db_item.amount_in_inventory - 5
    assert updated_item.amount_in_stash == original_db_item.amount_in_stash + 5


async def test_update_any_inventory_quantity(test_session, db_user, db_inventory_item):
    """Test updating quantity."""
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=10, amount_in_stash=0)
    original_db_item = inventory_item.copy()
    updated_item = await user_inv_crud.update_any_inventory_quantity(db_user.id, 3, inventory_item)
    assert updated_item.amount_in_stash == original_db_item.amount_in_stash + 3


async def test_new_inventory_item(test_session, db_user):
    """Test adding or updating user inventory item."""
    item = ItemsFactory()
    test_session.add(item)
    await test_session.commit()
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    new_item = await user_inv_crud.update_user_inventory_item(db_user.id, item.id, 10, to_stash=False)
    assert new_item.amount_in_inventory == 10
    assert new_item.amount_in_stash == 0


async def test_new_user_stash_item(test_session, db_user):
    """Test adding new inventory item."""
    item = ItemsFactory()
    test_session.add(item)
    await test_session.commit()
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    new_item = await user_inv_crud.update_user_inventory_item(db_user.id, item.id, 10, to_stash=True)
    assert new_item.amount_in_stash == 10
    assert new_item.amount_in_inventory == 0
    assert new_item.item_name == item.item_name


async def test_get_all_items_by_inventory_id(test_session, db_user, db_inventory_item):
    """Test retrieving all items from a user inventory."""
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=10, amount_in_stash=0)
    all_items = await user_inv_crud.get_all_items_by_inventory_id(db_user.inventory.id)
    assert len(all_items) == 1
    assert all_items[0].id == inventory_item.id


async def test_multiple_inventory_items(test_session, db_user, db_inventory_item):
    """Test case for handling multiple unique inventory items."""
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    item1 = await db_inventory_item(amount_in_inventory=5, amount_in_stash=0)
    item2 = await db_inventory_item(amount_in_inventory=0, amount_in_stash=10)
    item3 = await db_inventory_item(amount_in_inventory=3, amount_in_stash=7)
    all_items = await user_inv_crud.get_all_items_by_inventory_id(db_user.inventory.id)
    assert len(all_items) == 3
    assert all_items[0].amount_in_inventory == 5
    assert all_items[0].item_id == item1.item_id
    assert all_items[0].id == item1.id
    assert all_items[0].item_name == item1.item_name
    assert all_items[1].amount_in_stash == 10
    assert all_items[2].amount_in_inventory == 3
    assert all_items[2].amount_in_stash == 7


async def test_switch_item_stash_status_edge_cases(test_session, db_user, db_inventory_item):
    """Test switching stash status with max and zero quantities."""
    inventory_item = await db_inventory_item(amount_in_inventory=10, amount_in_stash=0)
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    updated_item = await user_inv_crud.switch_item_stash_status(
        db_user.id, inventory_item.id, to_stash=True, quantity=10
    )
    assert updated_item.amount_in_inventory == 0
    assert updated_item.amount_in_stash == 10
    with pytest.raises(ValueError):
        await user_inv_crud.switch_item_stash_status(
            db_user.id, inventory_item.id, to_stash=True, quantity=5
        )
    updated_item = await user_inv_crud.switch_item_stash_status(
        db_user.id, inventory_item.id, to_stash=False, quantity=10
    )
    assert updated_item.amount_in_inventory == 10
    assert updated_item.amount_in_stash == 0


async def test_update_any_inventory_quantity_negative(test_session, db_user, db_inventory_item):
    """Test updating inventory with negative quantities."""
    inventory_item = await db_inventory_item(amount_in_inventory=5, amount_in_stash=0)
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    updated_item = await user_inv_crud.update_any_inventory_quantity(db_user.id, -3, inventory_item)
    assert updated_item.amount_in_inventory == 2
    with pytest.raises(ValueError):
        await user_inv_crud.update_any_inventory_quantity(db_user.id, -5, inventory_item)


async def test_update_user_inventory_item_new_creation(test_session, db_user):
    """Test adding a new item to the user inventory."""
    item = ItemsFactory()
    test_session.add(item)
    await test_session.commit()
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    new_item = await user_inv_crud.update_user_inventory_item(db_user.id, item.id, 5, to_stash=False)
    assert new_item.amount_in_inventory == 5
    assert new_item.amount_in_stash == 0


async def test_remove_items_until_zero(test_session, db_user, db_inventory_item):
    """Test removing items until inventory reaches zero."""
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=10, amount_in_stash=0)
    updated_item = await user_inv_crud.update_any_inventory_quantity(db_user.id, -5, inventory_item)
    assert updated_item.amount_in_inventory == 5
    await user_inv_crud.update_any_inventory_quantity(db_user.id, -5, inventory_item)
    get_updated_item = await user_inv_crud.get_inventory_item_by_userid(db_user.id, inventory_item.id)
    assert get_updated_item is None


async def test_switch_item_stash_status_boundary_conditions(test_session, db_user, db_inventory_item):
    """Test switching stash status with various boundary conditions."""
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=5, amount_in_stash=0)
    updated_item = await user_inv_crud.switch_item_stash_status(
        db_user.id, inventory_item.id, to_stash=True, quantity=5
    )
    assert updated_item.amount_in_inventory == 0
    assert updated_item.amount_in_stash == 5
    with pytest.raises(ValueError, match="Not enough quantity available"):
        await user_inv_crud.switch_item_stash_status(db_user.id, inventory_item.id, to_stash=False, quantity=6)


async def test_invalid_item_modifications(test_session, db_user, db_inventory_item):
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    inventory_item = await db_inventory_item(
        amount_in_inventory=5, is_modified=True, modifications={'test': 'test'}
    )
    with pytest.raises(ValueError, match="Cannot reduce quantity of modified items"):
        await user_inv_crud.update_user_inventory_item(db_user.id, inventory_item.item_id, -1)


async def test_invalid_quantity_updates(test_session, db_user):
    """Test adding invalid quantities (negative or zero)."""
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    item = ItemsFactory()
    test_session.add(item)
    await test_session.commit()
    with pytest.raises(ValueError, match="Cannot add zero or negative quantity"):
        await user_inv_crud.update_user_inventory_item(db_user.id, item.id, 0)
    with pytest.raises(ValueError, match="Cannot add zero or negative quantity"):
        await user_inv_crud.update_user_inventory_item(db_user.id, item.id, -5)


async def test_item_deletion_when_quantity_zero(test_session, db_user, db_inventory_item):
    """Test that an item is deleted when its quantity reaches zero."""
    user_inv_crud = UserInventoryCRUD(Inventory, test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=3, amount_in_stash=2)
    await user_inv_crud.update_any_inventory_quantity(db_user.id, -3, inventory_item)
    await user_inv_crud.update_any_inventory_quantity(db_user.id, -2, inventory_item)
    assert await user_inv_crud.get_inventory_item_by_userid(db_user.id, inventory_item.id) is None
