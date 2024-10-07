import pytest
from unittest.mock import AsyncMock, Mock
from app.game_systems.items.item_stats_handler import ItemStatsHandler
from app.models.models import Stats, Inventory, InventoryItem, User
from app.models.item_models import Items, Clothing, Armor
from app.models.weapon_models import Weapon
from app.schemas import ItemType, ClothingType, ArmorType


@pytest.fixture
def mock_weapon_details():
    weapon_details = Mock()
    weapon_details.damage = 10
    weapon_details.strength_adj = 2
    weapon_details.agility_adj = 1
    return weapon_details


@pytest.fixture
def handler(mock_inventory, mock_user, mock_stats, mock_inventory_item, mock_item, mock_weapon_details):
    handler = ItemStatsHandler(user_id=1, inventory_item_id=1, session=AsyncMock())
    handler.get_user_data = AsyncMock(return_value=(mock_user, mock_inventory, mock_stats, mock_inventory_item))
    handler.get_item_data = AsyncMock(return_value=(mock_item, mock_weapon_details))
    handler.determine_slot = Mock(return_value="equipped_weapon_id")
    handler.update_equipped_status = AsyncMock()
    handler.adjust_user_stats = AsyncMock()
    return handler


@pytest.fixture
def unequip_handler(handler, mock_inventory, mock_user, mock_stats, mock_inventory_item, mock_item, mock_weapon_details):
    handler.get_user_data = AsyncMock(return_value=(mock_user, mock_inventory, mock_stats, mock_inventory_item))
    handler.get_item_data = AsyncMock(return_value=(mock_item, mock_weapon_details))
    handler.determine_slot = Mock(return_value="equipped_weapon_id")
    handler.update_equipped_status = AsyncMock()
    handler.adjust_user_stats = AsyncMock()
    mock_inventory.equipped_weapon_id = 1
    mock_inventory_item.one_equipped = True
    mock_inventory_item.amount_in_inventory = 1
    return handler


@pytest.fixture
def mock_item_stats_handler():
    return ItemStatsHandler(user_id=1, inventory_item_id=1, session=AsyncMock())



class TestEquip:

    async def test_calls_get_user_data(self, handler):
        await handler.equip_item()
        handler.get_user_data.assert_awaited_once()


    async def test_calls_get_item_data(self, handler, mock_inventory_item):
        await handler.equip_item()
        handler.get_item_data.assert_awaited_once_with(mock_inventory_item)


    async def test_calls_determine_slot(self, handler, mock_item, mock_weapon_details):
        await handler.equip_item()
        handler.determine_slot.assert_called_once_with(mock_item, mock_weapon_details)


    async def test_calls_update_equipped_status(self, handler, mock_inventory, mock_inventory_item):
        await handler.equip_item()
        handler.update_equipped_status.assert_awaited_once_with(mock_inventory, "equipped_weapon_id", mock_inventory_item, True)


    async def test_calls_adjust_user_stats(self, handler, mock_stats, mock_weapon_details):
        await handler.equip_item()
        handler.adjust_user_stats.assert_awaited_once_with(mock_stats, mock_weapon_details, equip=True)


    async def test_returns_correct_data_structure(self, handler, mock_stats, mock_inventory, mock_inventory_item):
        result = await handler.equip_item()
        assert 'stats' in result
        assert 'user-inventory' in result
        assert 'equipped-item' in result
        assert result['stats'] == mock_stats
        assert result['user-inventory'] == mock_inventory
        assert result['equipped-item'] == mock_inventory_item


    async def test_item_not_in_inventory(self, handler, mock_inventory_item):
        mock_inventory_item.amount_in_inventory = 0
        with pytest.raises(ValueError, match="Item not found in inventory"):
            await handler.equip_item()


    async def test_item_already_equipped(self, handler, mock_inventory_item):
        mock_inventory_item.one_equipped = True
        with pytest.raises(ValueError, match="Item is already equipped"):
            await handler.equip_item()


    async def test_item_cannot_be_equipped(self, handler):
        handler.determine_slot = Mock(return_value=None)
        with pytest.raises(ValueError, match="This item cannot be equipped"):
            await handler.equip_item()


    async def test_unequips_existing_item(self, handler, mock_inventory):
        mock_inventory.equipped_weapon_id = 2
        handler.unequip_item = AsyncMock(return_value=Mock())
        result = await handler.equip_item()
        handler.unequip_item.assert_awaited_once_with(2, called_from_equip=True)
        assert 'unequipped-item' in result


    async def test_when_no_item_equipped(self, handler, mock_inventory):
        mock_inventory.equipped_weapon_id = None
        handler.unequip_item = AsyncMock()
        await handler.equip_item()
        handler.unequip_item.assert_not_awaited()


    async def test_with_different_item_types(self, handler, mock_item, mock_weapon_details):
        for item_type in [ItemType.Clothing, ItemType.Armor]:
            mock_item.category = item_type
            await handler.equip_item()
            handler.determine_slot.assert_called_with(mock_item, mock_weapon_details)


    async def test_with_one_quantity(self, handler, mock_stats, mock_inventory, mock_inventory_item):
        mock_inventory_item.amount_in_inventory = 1
        result_first = await handler.equip_item()
        assert 'stats' in result_first
        assert 'user-inventory' in result_first
        assert 'equipped-item' in result_first
        assert result_first['stats'] == mock_stats
        assert result_first['user-inventory'] == mock_inventory


    async def test_with_invalid_item_type(self, handler, mock_item):
        mock_item.category = 'InvalidType'
        handler.determine_slot = Mock(return_value=None)
        with pytest.raises(ValueError, match="This item cannot be equipped"):
            await handler.equip_item()



class TestUnequip:

    async def test_item_calls_get_user_data(self, unequip_handler):
        await unequip_handler.unequip_item()
        unequip_handler.get_user_data.assert_awaited_once()


    async def test_item_calls_get_item_data(self, unequip_handler, mock_inventory_item):
        await unequip_handler.unequip_item()
        unequip_handler.get_item_data.assert_awaited_once_with(mock_inventory_item)


    async def test_item_calls_determine_slot(self, unequip_handler, mock_item, mock_weapon_details):
        await unequip_handler.unequip_item()
        unequip_handler.determine_slot.assert_called_once_with(mock_item, mock_weapon_details)


    async def test_item_calls_update_equipped_status(self, unequip_handler, mock_inventory, mock_inventory_item):
        await unequip_handler.unequip_item()
        unequip_handler.update_equipped_status.assert_awaited_once_with(mock_inventory, "equipped_weapon_id", mock_inventory_item, False)


    async def test_item_calls_adjust_user_stats(self, unequip_handler, mock_stats, mock_weapon_details):
        await unequip_handler.unequip_item()
        unequip_handler.adjust_user_stats.assert_awaited_once_with(mock_stats, mock_weapon_details, equip=False)


    async def test_item_returns_correct_data_structure(self, unequip_handler, mock_stats, mock_inventory, mock_inventory_item):
        result = await unequip_handler.unequip_item()
        assert 'stats' in result
        assert 'user-inventory' in result
        assert 'unequipped-item' in result
        assert result['stats'] == mock_stats
        assert result['user-inventory'] == mock_inventory
        assert result['unequipped-item'] == mock_inventory_item


    async def test_item_item_cannot_be_equipped(self, unequip_handler):
        unequip_handler.determine_slot = Mock(return_value=None)
        with pytest.raises(ValueError, match="This item cannot be equipped"):
            await unequip_handler.unequip_item()


    async def test_item_not_equipped(self, unequip_handler, mock_inventory_item):
        mock_inventory_item.one_equipped = False
        with pytest.raises(ValueError, match="Item is not equipped"):
            await unequip_handler.unequip_item()


    async def test_item_with_specific_inventory_item_id(self, unequip_handler):
        specific_id = 5
        await unequip_handler.unequip_item(inventory_item_id=specific_id)
        unequip_handler.get_user_data.assert_awaited_once_with(specific_id)


    async def test_item_called_from_equip(self, unequip_handler, mock_inventory_item):
        result = await unequip_handler.unequip_item(called_from_equip=True)
        assert isinstance(result, Mock)
        assert result == mock_inventory_item


    async def test_item_updates_inventory_item(self, unequip_handler, mock_inventory_item, mock_inventory):
        await unequip_handler.unequip_item()
        unequip_handler.update_equipped_status.assert_awaited_once_with(
            mock_inventory, "equipped_weapon_id", mock_inventory_item, False
        )


    async def test_item_clears_equipped_slot(self, unequip_handler, mock_inventory, mock_inventory_item):
        await unequip_handler.unequip_item()
        unequip_handler.update_equipped_status.assert_awaited_once_with(
            mock_inventory, "equipped_weapon_id", mock_inventory_item, False
        )


    async def test_item_with_different_item_types(self, unequip_handler, mock_item, mock_weapon_details):
        for item_type in [ItemType.Clothing, ItemType.Armor, ItemType.Weapon]:
            mock_item.category = item_type
            await unequip_handler.unequip_item()
            unequip_handler.determine_slot.assert_called_with(mock_item, mock_weapon_details)


    async def test_last_item(self, unequip_handler, mock_inventory, mock_inventory_item):
        mock_inventory_item.amount_in_inventory = 0
        mock_inventory_item.one_equipped = True
        await unequip_handler.unequip_item()
        unequip_handler.update_equipped_status.assert_awaited_once_with(
            mock_inventory, "equipped_weapon_id", mock_inventory_item, False
        )


    async def test_item_with_invalid_item_type(self, unequip_handler, mock_item):
        mock_item.category = 'InvalidType'
        unequip_handler.determine_slot = Mock(return_value=None)
        with pytest.raises(ValueError, match="This item cannot be equipped"):
            await unequip_handler.unequip_item()



class TestGetUserData:

    @pytest.fixture
    def get_user_data_handler(self):
        mock_session = AsyncMock()
        mock_user_inventory_crud = AsyncMock()
        handler = ItemStatsHandler(user_id=1, inventory_item_id=1, session=mock_session)
        handler.user_inventory_crud = mock_user_inventory_crud
        return handler


    async def test_with_existing_data(self, get_user_data_handler):
        get_user_data_handler.user = Mock(spec=User)
        get_user_data_handler.inventory = Mock(spec=Inventory)
        get_user_data_handler.stats = Mock(spec=Stats)
        mock_inventory_item = Mock(spec=InventoryItem)
        get_user_data_handler.user_inventory_crud.get_inventory_item_by_userid.return_value = mock_inventory_item
        result = await get_user_data_handler.get_user_data()
        assert result == (
            get_user_data_handler.user,
            get_user_data_handler.inventory,
            get_user_data_handler.stats, mock_inventory_item
        )
        get_user_data_handler.user_inventory_crud.get_inventory_item_by_userid.assert_awaited_once_with(1, 1)


    async def test_without_existing_data(self, get_user_data_handler):
        mock_user = Mock(spec=User)
        mock_inventory = Mock(spec=Inventory)
        mock_stats = Mock(spec=Stats)
        mock_inventory_item = Mock(spec=InventoryItem)
        get_user_data_handler.user_inventory_crud.get_inventory_item_by_userid.return_value = mock_inventory_item
        get_user_data_handler.session.get.side_effect = [mock_user, mock_inventory, mock_stats]
        result = await get_user_data_handler.get_user_data()
        assert result == (mock_user, mock_inventory, mock_stats, mock_inventory_item)
        get_user_data_handler.user_inventory_crud.get_inventory_item_by_userid.assert_awaited_once_with(1, 1)
        assert get_user_data_handler.session.get.await_count == 3


    async def test_with_specific_inventory_item_id(self, get_user_data_handler):
        mock_inventory_item = Mock(spec=InventoryItem)
        get_user_data_handler.user_inventory_crud.get_inventory_item_by_userid.return_value = mock_inventory_item
        await get_user_data_handler.get_user_data(inventory_item_id=5)
        get_user_data_handler.user_inventory_crud.get_inventory_item_by_userid.assert_awaited_once_with(1, 5)


    async def test_item_not_found(self, get_user_data_handler):
        get_user_data_handler.user_inventory_crud.get_inventory_item_by_userid.return_value = None
        with pytest.raises(LookupError, match="Item not found in inventory"):
            await get_user_data_handler.get_user_data()


    async def test_user_not_found(self, get_user_data_handler):
        mock_inventory_item = Mock(spec=InventoryItem)
        get_user_data_handler.user_inventory_crud.get_inventory_item_by_userid.return_value = mock_inventory_item
        get_user_data_handler.session.get.return_value = None
        with pytest.raises(LookupError, match="User not found"):
            await get_user_data_handler.get_user_data()


    async def test_caches_user_data(self, get_user_data_handler):
        mock_user = Mock(spec=User)
        mock_inventory = Mock(spec=Inventory)
        mock_stats = Mock(spec=Stats)
        mock_inventory_item = Mock(spec=InventoryItem)
        get_user_data_handler.user_inventory_crud.get_inventory_item_by_userid.return_value = mock_inventory_item
        get_user_data_handler.session.get.side_effect = [mock_user, mock_inventory, mock_stats]
        await get_user_data_handler.get_user_data()
        await get_user_data_handler.get_user_data()
        assert get_user_data_handler.session.get.await_count == 3
        assert get_user_data_handler.user == mock_user
        assert get_user_data_handler.inventory == mock_inventory
        assert get_user_data_handler.stats == mock_stats



class TestGetItemData:

    async def test_get_item_data_success(self, mock_item_stats_handler, mock_inventory_item, mock_item):
        mock_item_details = Mock(spec=(Clothing, Weapon, Armor))
        mock_item_stats_handler.session.get = AsyncMock(return_value=mock_item)
        mock_item_stats_handler.get_item_details = AsyncMock(return_value=mock_item_details)
        result = await mock_item_stats_handler.get_item_data(mock_inventory_item)
        mock_item_stats_handler.session.get.assert_awaited_once_with(Items, mock_inventory_item.item_id)
        mock_item_stats_handler.get_item_details.assert_awaited_once_with(mock_item)
        assert result == (mock_item, mock_item_details)


    async def test_get_item_data_item_not_found(self, mock_item_stats_handler, mock_inventory_item):
        mock_item_stats_handler.session.get = AsyncMock(return_value=None)
        with pytest.raises(LookupError, match="Item not found"):
            await mock_item_stats_handler.get_item_data(mock_inventory_item)


    async def test_get_item_data_details_not_available(self, mock_item_stats_handler, mock_inventory_item, mock_item):
        mock_item_stats_handler.session.get = AsyncMock(return_value=mock_item)
        mock_item_stats_handler.get_item_details = AsyncMock(return_value=None)
        with pytest.raises(LookupError, match="Item details not available"):
            await mock_item_stats_handler.get_item_data(mock_inventory_item)


    async def test_get_item_data_with_clothing(self, mock_item_stats_handler, mock_inventory_item, mock_item):
        mock_clothing = Mock(spec=Clothing)
        mock_item_stats_handler.session.get = AsyncMock(return_value=mock_item)
        mock_item_stats_handler.get_item_details = AsyncMock(return_value=mock_clothing)
        result = await mock_item_stats_handler.get_item_data(mock_inventory_item)
        assert isinstance(result[1], Clothing)


    async def test_get_item_data_with_weapon(self, mock_item_stats_handler, mock_inventory_item, mock_item):
        mock_weapon = Mock(spec=Weapon)
        mock_item_stats_handler.session.get = AsyncMock(return_value=mock_item)
        mock_item_stats_handler.get_item_details = AsyncMock(return_value=mock_weapon)
        result = await mock_item_stats_handler.get_item_data(mock_inventory_item)
        assert isinstance(result[1], Weapon)


    async def test_get_item_data_with_armor(self, mock_item_stats_handler, mock_inventory_item, mock_item):
        mock_armor = Mock(spec=Armor)
        mock_item_stats_handler.session.get = AsyncMock(return_value=mock_item)
        mock_item_stats_handler.get_item_details = AsyncMock(return_value=mock_armor)
        result = await mock_item_stats_handler.get_item_data(mock_inventory_item)
        assert isinstance(result[1], Armor)



class TestStatsHandlerUtils:

    async def test_update_equipped_status_equip(self, mock_item_stats_handler, mock_inventory, mock_inventory_item):
        await mock_item_stats_handler.update_equipped_status(mock_inventory, "equipped_weapon_id", mock_inventory_item, True)
        assert mock_inventory.equipped_weapon_id == mock_inventory_item.id
        assert mock_inventory_item.one_equipped is True
        assert mock_inventory_item.amount_in_inventory == 0
        mock_item_stats_handler.session.flush.assert_awaited_once()


    async def test_update_equipped_status_unequip(self, mock_item_stats_handler, mock_inventory, mock_inventory_item):
        mock_inventory_item.one_equipped = True
        mock_inventory_item.amount_in_inventory = 0
        await mock_item_stats_handler.update_equipped_status(mock_inventory, "equipped_weapon_id", mock_inventory_item, False)
        assert mock_inventory.equipped_weapon_id is None
        assert mock_inventory_item.one_equipped is False
        assert mock_inventory_item.amount_in_inventory == 1
        mock_item_stats_handler.session.flush.assert_awaited_once()

    @pytest.fixture
    def real_stats(self):
        return Stats(
            reputation=10.0,
            max_energy=100,
            strength=1.0,
            agility=1.0
        )

    class MockWeapon:
        def __init__(self):
            self.damage = 10
            self.strength_adj = 2
            self.agility_adj = 1

    @pytest.fixture
    def mock_weapon_details(self):
        return self.MockWeapon()


    async def test_adjust_user_stats_equip(self, mock_item_stats_handler, real_stats, mock_weapon_details):
        mock_item_stats_handler.get_adj_wrapper = Mock(return_value={
            "strength": "strength_adj",
            "agility": "agility_adj"
        })
        await mock_item_stats_handler.adjust_user_stats(real_stats, mock_weapon_details, equip=True)
        assert real_stats.strength == 3  # default 1 + 2
        assert real_stats.agility == 2  # default 1 + 1


    async def test_adjust_user_stats_unequip(self, mock_item_stats_handler, real_stats, mock_weapon_details):
        mock_item_stats_handler.get_adj_wrapper = Mock(return_value={
            "strength": "strength_adj",
            "agility": "agility_adj"
        })

        real_stats.strength = 5
        real_stats.agility = 2
        await mock_item_stats_handler.adjust_user_stats(real_stats, mock_weapon_details, equip=False)
        assert real_stats.strength == 3  # 5 - 2
        assert real_stats.agility == 1  # 2 - 1


    def test_determine_slot_weapon(self, mock_item_stats_handler, mock_item, mock_weapon_details):
        mock_item.category = ItemType.Weapon
        assert mock_item_stats_handler.determine_slot(mock_item, mock_weapon_details) == "equipped_weapon_id"


    def test_determine_slot_clothing(self, mock_item_stats_handler, mock_item):
        mock_item.category = ItemType.Clothing
        mock_clothing_details = Mock(clothing_type=ClothingType.Mask)
        assert mock_item_stats_handler.determine_slot(mock_item, mock_clothing_details) == "equipped_mask_id"


    def test_determine_slot_armor(self, mock_item_stats_handler, mock_item):
        mock_item.category = ItemType.Armor
        mock_armor_details = Mock(type=ArmorType.Head)
        assert mock_item_stats_handler.determine_slot(mock_item, mock_armor_details) == "equipped_head_armor_id"


    def test_get_adj_wrapper_clothing(self, mock_item_stats_handler):
        mock_clothing = Mock(spec=Clothing)
        wrapper = mock_item_stats_handler.get_adj_wrapper(mock_clothing)
        assert "reputation" in wrapper
        assert wrapper["reputation"] == "reputation_adj"


    def test_get_adj_wrapper_armor(self, mock_item_stats_handler):
        mock_armor = Mock(spec=Armor)
        wrapper = mock_item_stats_handler.get_adj_wrapper(mock_armor)
        assert "head_protection" in wrapper
        assert wrapper["head_protection"] == "head_protection_adj"


    def test_get_adj_wrapper_weapon(self, mock_item_stats_handler):
        mock_weapon = Mock(spec=Weapon)
        wrapper = mock_item_stats_handler.get_adj_wrapper(mock_weapon)
        assert "strength" in wrapper
        assert wrapper["strength"] == "strength_adj"


    async def test_get_item_details_clothing(self, mock_item_stats_handler, mock_item):
        mock_item.category = ItemType.Clothing
        mock_item.clothing_details = Mock()
        mock_item_stats_handler.session.refresh = AsyncMock()
        result = await mock_item_stats_handler.get_item_details(mock_item)
        assert result == mock_item.clothing_details
        mock_item_stats_handler.session.refresh.assert_awaited_once_with(
            mock_item, ["clothing_details", "weapon_details", "armor_details"]
        )

    async def test_get_item_details_weapon(self, mock_item_stats_handler, mock_item):
        mock_item.category = ItemType.Weapon
        mock_item.weapon_details = Mock()
        mock_item_stats_handler.session.refresh = AsyncMock()
        result = await mock_item_stats_handler.get_item_details(mock_item)
        assert result == mock_item.weapon_details
        mock_item_stats_handler.session.refresh.assert_awaited_once_with(
            mock_item, ["clothing_details", "weapon_details", "armor_details"]
        )

    async def test_get_item_details_armor(self, mock_item_stats_handler, mock_item):
        mock_item.category = ItemType.Armor
        mock_item.armor_details = Mock()
        mock_item_stats_handler.session.refresh = AsyncMock()
        result = await mock_item_stats_handler.get_item_details(mock_item)
        assert result == mock_item.armor_details
        mock_item_stats_handler.session.refresh.assert_awaited_once_with(
            mock_item, ["clothing_details", "weapon_details", "armor_details"]
        )

    async def test_get_item_details_invalid_category(self, mock_item_stats_handler, mock_item):
        mock_item.category = "InvalidCategory"
        mock_item_stats_handler.session.refresh = AsyncMock()
        result = await mock_item_stats_handler.get_item_details(mock_item)
        assert result is None
        mock_item_stats_handler.session.refresh.assert_awaited_once_with(
            mock_item, ["clothing_details", "weapon_details", "armor_details"]
        )
