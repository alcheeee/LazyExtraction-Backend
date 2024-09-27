import pytest
from app.models import User, InventoryItem
from model_factories import (
    UserFactory,
    InventoryFactory,
    StatsFactory,
    TrainingProgressFactory,
    InventoryItemFactory,
    ItemsFactory
)


@pytest.fixture
def temp_user():
    def _temp_user() -> User:
        user = UserFactory()
        user.inventory = InventoryFactory()
        user.stats = StatsFactory()
        user.training_progress = TrainingProgressFactory()
        return user

    return _temp_user


@pytest.fixture
async def db_user(test_session, temp_user) -> User:
    user = temp_user()
    test_session.add(user)
    await test_session.commit()
    return user


@pytest.fixture
async def db_inventory_item(test_session, db_user):
    async def _db_inventory_item(
            amount_in_inventory: int = 0,
            amount_in_stash: int = 0,
            one_equipped: bool = False,
            is_modified: bool = False,
            modifications: dict = None,
            item_data: dict = None,
            user=db_user
    ) -> InventoryItem:
        item = ItemsFactory(**(item_data or {}))
        inventory_item = InventoryItemFactory(
            inventory=user.inventory,
            item=item,
            amount_in_inventory=amount_in_inventory,
            amount_in_stash=amount_in_stash,
            one_equipped=one_equipped,
            is_modified=is_modified,
            modifications=modifications
        )
        test_session.add(inventory_item)
        await test_session.commit()
        return inventory_item

    return _db_inventory_item
