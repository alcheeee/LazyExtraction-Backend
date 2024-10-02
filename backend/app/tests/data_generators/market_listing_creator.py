from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from app.models import (
    MarketItems
)


fake = Faker()


async def create_market_items(session: AsyncSession, items, users, market_listings):
    for _ in range(market_listings):
        item = fake.random_element(items)
        user = fake.random_element(users)
        market_item = MarketItems(
            item_name=item.item_name,
            item_cost=fake.random_int(10, 10000),
            quick_sell_value=item.quick_sell,
            item_quantity=fake.random_int(1, 10),
            by_user=user.username,
            posted_at=fake.date_time_between(start_date="-30d", end_date="now"),
            is_modified=fake.boolean(chance_of_getting_true=30),
            modifications={},
            item=item
        )
        session.add(market_item)
    await session.flush()
