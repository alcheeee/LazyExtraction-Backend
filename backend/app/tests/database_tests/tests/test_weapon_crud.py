import pytest
from app.crud.weapon_crud import WeaponCRUD
from app.models import InventoryItem, Items, Inventory, User, Weapon, Attachments
from app.schemas import AttachmentTypes
from app.tests.database_tests.model_factories import (
    InventoryItemFactory,
    ItemsFactory
)


@pytest.fixture
async def db_weapon(test_session) -> Items:
    weapon_item = ItemsFactory(
        category="Weapon"
    )
    weapon_details = Weapon(
        damage=20,
        strength_adj=10,
        range=10,
        accuracy=10,
        reload_speed=10,
        fire_rate=10,
        magazine_size=10,
        armor_penetration=10,
        headshot_chance=10,
        agility_adj=-10,
    )
    weapon_item.weapon_details = weapon_details
    test_session.add(weapon_item)
    await test_session.flush()
    return weapon_item


@pytest.fixture
async def db_inventory_item_weapon(test_session, db_user, db_weapon):
    inventory_item = InventoryItemFactory(
        inventory_id=db_user.inventory_id,
        item_id=db_weapon.id,
        item=db_weapon,
        amount_in_inventory=1,
        amount_in_stash=0
    )
    test_session.add(inventory_item)
    await test_session.flush()
    return inventory_item


async def test_get_user_weapon(test_session, db_user, db_inventory_item_weapon):
    """Test retrieving weapon by user inventory id and weapon inventory id."""
    weapon_crud = WeaponCRUD(test_session)
    fetched_item, fetched_inv_item = await weapon_crud.get_user_weapon(
        db_user.inventory_id,
        db_inventory_item_weapon.id
    )
    assert fetched_item.id == db_inventory_item_weapon.item_id
    assert fetched_inv_item.id == db_inventory_item_weapon.id
    assert fetched_inv_item.item_name == db_inventory_item_weapon.item_name
    assert fetched_item.weapon_details is not None



async def test_update_weapon_for_attachments(test_session, db_user, db_inventory_item):
    """Test switching item stash status."""
    weapon_crud = WeaponCRUD(test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=10, amount_in_stash=0)
    original_db_item = inventory_item.copy()
    new_item, updated_item = await weapon_crud.update_weapon_for_attachments(
        db_user.id,
        inventory_item
    )
    assert new_item is not None
    assert updated_item is not None
    assert new_item.id != original_db_item.id
    assert updated_item.id == original_db_item.id
    assert new_item.item_name == original_db_item.item_name == updated_item.item_name
    assert new_item.is_modified is True
    assert updated_item.is_modified is False
    assert new_item.amount_in_stash == 1
    assert new_item.amount_in_inventory == 0
    assert updated_item.amount_in_inventory == 9
    assert updated_item.amount_in_stash == 0


async def test_update_weapon_for_attachments_weight_change(test_session, db_user, db_inventory_item):
    weapon_crud = WeaponCRUD(test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=1, item_data={"weight": 2.0})
    db_user.inventory.current_weight = 100.0
    initial_weight = db_user.inventory.current_weight
    new_item, updated_item = await weapon_crud.update_weapon_for_attachments(db_user.id, inventory_item)
    assert new_item.id != inventory_item.id
    assert db_user.inventory.current_weight == initial_weight - 2.0


async def test_update_weapon_for_attachments_delete_original(test_session, db_user, db_inventory_item):
    weapon_crud = WeaponCRUD(test_session)
    inventory_item = await db_inventory_item(amount_in_inventory=1, amount_in_stash=0)
    new_item, updated_item = await weapon_crud.update_weapon_for_attachments(db_user.id, inventory_item)
    assert new_item is not None
    assert updated_item is None
    assert await test_session.get(type(inventory_item), inventory_item.id) is None

