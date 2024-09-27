import pytest
import factory
from faker import Faker
from app.crud.market_crud import MarketCRUD
from app.models import MarketItems, Items
from app.schemas import MarketTransactionRequest


fake = Faker()


class ItemsFactory(factory.Factory):
    class Meta:
        model = Items

    id = factory.Sequence(lambda n: n)
    item_name = factory.LazyAttribute(lambda _: fake.word())

class MarketItemsFactory(factory.Factory):
    class Meta:
        model = MarketItems

    id = factory.Sequence(lambda n: n)
    item = factory.SubFactory(ItemsFactory)

    item_name = factory.LazyAttribute(lambda obj: obj.item.item_name)
    item_cost = 100
    quick_sell_value = 10
    item_quantity = 1
    by_user = factory.LazyAttribute(lambda _: fake.user_name())
    item_id = factory.SelfAttribute('item.id')


async def test_get_market_item_from_market_id(test_session):
    """Test retrieving market item by its market ID"""
    market_crud = MarketCRUD(MarketItems, test_session)
    test_market_item = MarketItemsFactory()
    test_session.add(test_market_item)
    await test_session.commit()
    market_item = await market_crud.get_market_item_from_market_id(test_market_item.id)
    assert market_item.id == test_market_item.id
    assert market_item.item_id is not None


async def test_get_non_existent_market_item(test_session):
    """Test retrieving non-existent market item by its market ID"""
    market_crud = MarketCRUD(MarketItems, test_session)
    random_item = ItemsFactory()
    with pytest.raises(LookupError, match="Item not found"):
        await market_crud.get_market_item_from_market_id(random_item.id)


async def test_get_all_market_items_by_name(test_session):
    """Test retrieving market items by item name"""
    market_crud = MarketCRUD(MarketItems, test_session)
    test_market_item = MarketItemsFactory()
    test_session.add(test_market_item)
    await test_session.commit()
    market_items = await market_crud.get_all_market_items_by_name(test_market_item.item_name)
    assert len(market_items) == 1
    assert market_items[0].item_name == test_market_item.item_name


async def test_get_all_market_items_by_name_multiple(test_session):
    """Test retrieving multiple market items by item name"""
    market_crud = MarketCRUD(MarketItems, test_session)
    test_market_item1 = MarketItemsFactory()
    test_market_item2 = MarketItemsFactory(item_name=test_market_item1.item_name)
    test_session.add(test_market_item1)
    test_session.add(test_market_item2)
    await test_session.commit()
    market_items = await market_crud.get_all_market_items_by_name(test_market_item1.item_name)
    assert len(market_items) == 2
    assert all(item.item_name == test_market_item1.item_name for item in market_items)


async def test_get_empty_market_items(test_session):
    """Test retrieving non-existent market items by item name"""
    market_crud = MarketCRUD(MarketItems, test_session)
    random_item = ItemsFactory()
    market_items = await market_crud.get_all_market_items_by_name(random_item.item_name)
    assert len(market_items) == 0
    assert market_items == []


async def test_get_exact_market_item(test_session):
    """Test retrieving exact market item by id"""
    market_crud = MarketCRUD(MarketItems, test_session)
    test_market_item = MarketItemsFactory()
    test_session.add(test_market_item)
    await test_session.commit()
    exact_item = await market_crud.get_exact_market_item(test_market_item.id)
    assert exact_item is not None
    assert exact_item.item_id == test_market_item.item_id


async def test_get_non_existent_exact_market_item(test_session):
    """Test retrieving exact market item by id"""
    market_crud = MarketCRUD(MarketItems, test_session)
    random_item = ItemsFactory()
    exact_item = await market_crud.get_exact_market_item(random_item.id)
    assert exact_item is None
