from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from app.models import (
    InventoryItem,
    Items
)


fake = Faker()


async def populate_user_inventories(session: AsyncSession, users, items):
    for user in users:
        unmodified_items = {}
        total_weight = 0

        for _ in range(fake.random_int(5, 20)):
            item = fake.random_element(items)
            amount = fake.random_int(0, 15)
            is_modified = fake.boolean(chance_of_getting_true=30)

            if is_modified:
                inventory_item = InventoryItem(
                    item_name=item.item_name,
                    amount_in_inventory=amount,
                    is_modified=True,
                    quick_sell_value=item.quick_sell,
                    modifications={},
                    inventory=user.inventory,
                    item=item
                )
                session.add(inventory_item)
            else:
                if item.id in unmodified_items:
                    unmodified_items[item.id].amount_in_inventory += amount
                else:
                    unmodified_items[item.id] = InventoryItem(
                        item_name=item.item_name,
                        amount_in_inventory=amount,
                        is_modified=False,
                        quick_sell_value=item.quick_sell,
                        inventory=user.inventory,
                        item=item
                    )

            total_weight += item.weight * amount

        session.add_all(unmodified_items.values())
        user.inventory.current_weight = round(total_weight, 2)

    await session.flush()
