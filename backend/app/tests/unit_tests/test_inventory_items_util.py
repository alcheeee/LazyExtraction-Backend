import pytest
from unittest.mock import Mock
from app.models import InventoryItem, Items
from app.crud.crud_utilities.inventory_items_util import InventoryItemsCRUDUtils, AllowedArea


@pytest.mark.asyncio
async def test_handle_inventory_change_positive(mock_item):
    """Test handle_inventory_change with a positive quantity change."""
    mock_item.weight = 2.0
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=5, amount_in_stash=0, item=mock_item)
    result = await InventoryItemsCRUDUtils.handle_inventory_change(inv_item, AllowedArea.INVENTORY, 3)
    assert result == (8, 0, 6.0)  # (new_inventory_amount, new_stash_amount, weight_change)


@pytest.mark.asyncio
async def test_handle_inventory_change_any_area(mock_item):
    """Test handle_inventory_change with mixed stash/inventory quantities."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=3, amount_in_stash=2, item=mock_item)
    result = await InventoryItemsCRUDUtils.handle_inventory_change(inv_item, AllowedArea.ANY, -4)
    assert result == (1, 0, -4.0)


@pytest.mark.asyncio
async def test_handle_inventory_change_negative(mock_item):
    """Test handle_inventory_change with a negative quantity change."""
    mock_item.weight = 1.5
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=10, amount_in_stash=0, item=mock_item)
    result = await InventoryItemsCRUDUtils.handle_inventory_change(inv_item, AllowedArea.INVENTORY, -5)
    assert result == (5, 0, -7.5)


@pytest.mark.asyncio
async def test_handle_inventory_change_reduce_to_zero_equipped(mock_item):
    """Test reducing inventory to zero quantity when equipped."""
    mock_item.weight = 2.0
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=3, one_equipped=True, amount_in_stash=0, item=mock_item)
    result = await InventoryItemsCRUDUtils.handle_inventory_change(inv_item, AllowedArea.INVENTORY, -3)
    assert result == (0, 0, -6.0)


@pytest.mark.asyncio
async def test_handle_inventory_change_exceeding_stash(mock_item):
    """Test handle_inventory_change with quantity change exceeding stash."""
    mock_item.weight = 1.0
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=0, amount_in_stash=3, item=mock_item)
    result = await InventoryItemsCRUDUtils.handle_inventory_change(inv_item, AllowedArea.STASH, -2)
    assert result == (0, 1, -2.0)


@pytest.mark.asyncio
async def test_amount_handler_to_stash():
    """Test moving items from inventory to stash."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=10, amount_in_stash=0)
    new_inventory, new_stash = await InventoryItemsCRUDUtils.amount_handler(inv_item, AllowedArea.STASH, 5)
    assert new_inventory == 10
    assert new_stash == 5


@pytest.mark.asyncio
async def test_amount_handler_to_inventory():
    """Test moving items from stash to inventory."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=0, amount_in_stash=5)
    with pytest.raises(ValueError, match="Insufficient quantity available"):
        await InventoryItemsCRUDUtils.amount_handler(inv_item, AllowedArea.INVENTORY, -2)


@pytest.mark.asyncio
async def test_amount_handler_exceeding_quantity():
    """Test moving more items than available."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=3, amount_in_stash=0)
    with pytest.raises(ValueError, match="Insufficient quantity available"):
        await InventoryItemsCRUDUtils.amount_handler(inv_item, AllowedArea.ANY, -4)


@pytest.mark.asyncio
async def test_switch_item_location_to_stash():
    """Test switching items from inventory to stash."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=5, amount_in_stash=0)
    new_inventory, new_stash = await InventoryItemsCRUDUtils.switch_item_location(inv_item, to_stash=True, quantity=3)
    assert new_inventory == 2
    assert new_stash == 3


@pytest.mark.asyncio
async def test_switch_item_location_to_inventory():
    """Test switching items from stash to inventory."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=0, amount_in_stash=5)
    new_inventory, new_stash = await InventoryItemsCRUDUtils.switch_item_location(inv_item, to_stash=False, quantity=4)
    assert new_inventory == 4
    assert new_stash == 1


@pytest.mark.asyncio
async def test_switch_item_location_empty_stash():
    """Test switching from stash to inventory with an empty stash."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=2, amount_in_stash=0)
    with pytest.raises(ValueError, match="Not enough quantity in stash to move to inventory"):
        await InventoryItemsCRUDUtils.switch_item_location(inv_item, to_stash=False, quantity=1)


@pytest.mark.asyncio
async def test_switch_item_location_zero_quantities():
    """Test switching between stash and inventory with zero quantities."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=0, amount_in_stash=0)
    with pytest.raises(ValueError, match="Not enough quantity to switch"):
        await InventoryItemsCRUDUtils.switch_item_location(inv_item, to_stash=True, quantity=1)


@pytest.mark.asyncio
async def test_switch_item_location_not_enough_inventory():
    """Test trying to move more items to stash than available in inventory."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=2, amount_in_stash=0)
    with pytest.raises(ValueError, match="Not enough quantity to switch"):
        await InventoryItemsCRUDUtils.switch_item_location(inv_item, to_stash=True, quantity=5)


@pytest.mark.asyncio
async def test_validate_inventory_change_success():
    """Test valid inventory change."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=5, amount_in_stash=3)
    await InventoryItemsCRUDUtils.validate_inventory_change(inv_item, -3)


@pytest.mark.asyncio
async def test_validate_inventory_change_insufficient_quantity():
    """Test inventory change with insufficient quantity."""
    inv_item = Mock(spec=InventoryItem, amount_in_inventory=1, amount_in_stash=0)
    with pytest.raises(ValueError, match="Not enough quantity available"):
        await InventoryItemsCRUDUtils.validate_inventory_change(inv_item, -2)

