import pytest
from app.crud.items_crud import ItemsCRUD
from app.models import Items
from app.tests.database_tests.model_factories import ItemsFactory


async def test_get_item_from_name(test_session):
    """Test retrieving an item by its name."""
    items_crud = ItemsCRUD(Items, test_session)
    test_item = ItemsFactory()
    test_session.add(test_item)
    await test_session.commit()
    item = await items_crud.get_item_from_name(test_item.item_name)
    assert item is not None
    assert item.item_name == test_item.item_name


async def test_get_item_from_name_not_found(test_session):
    """Test retrieving an item by a name that does not exist."""
    items_crud = ItemsCRUD(Items, test_session)
    item = await items_crud.get_item_from_name("non_existent_item")
    assert item is None


async def test_get_item_field_from_id(test_session):
    """Test retrieving a specific field from an item by its ID."""
    items_crud = ItemsCRUD(Items, test_session)
    test_item = ItemsFactory()
    test_session.add(test_item)
    await test_session.commit()
    item_name = await items_crud.get_item_field_from_id(test_item.id, 'item_name')
    assert item_name == test_item.item_name


async def test_get_item_field_from_id_invalid_field(test_session):
    """Test retrieving a field that doesn't exist from an item."""
    items_crud = ItemsCRUD(Items, test_session)
    test_item = ItemsFactory()
    test_session.add(test_item)
    await test_session.commit()
    with pytest.raises(AttributeError):
        await items_crud.get_item_field_from_id(test_item.id, 'non_existent_field')


async def test_check_item_exists(test_session):
    """Test checking if an item exists by its name."""
    items_crud = ItemsCRUD(Items, test_session)
    test_item = ItemsFactory()
    test_session.add(test_item)
    await test_session.commit()
    result = await items_crud.check_item_exists(test_item.item_name)
    assert result is not None
    assert result == test_item.id


async def test_check_item_exists_not_found(test_session):
    """Test checking if an item exists with a non-existing name."""
    items_crud = ItemsCRUD(Items, test_session)
    result = await items_crud.check_item_exists("non_existent_item")
    assert result is None


async def test_get_item_name_by_id(test_session):
    """Test retrieving the item name by its ID."""
    items_crud = ItemsCRUD(Items, test_session)
    test_item = ItemsFactory()
    test_session.add(test_item)
    await test_session.commit()
    item_name = await items_crud.get_item_name_by_id(test_item.id)
    assert item_name == test_item.item_name


async def test_get_item_name_by_id_not_found(test_session):
    """Test retrieving an item name by an ID that does not exist."""
    items_crud = ItemsCRUD(Items, test_session)

    with pytest.raises(LookupError, match="Item not found"):
        await items_crud.get_item_name_by_id(999)