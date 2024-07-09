from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from ...models import Items


class BaseItemCreator:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_base_item(self, request):
        item_data = {
            "item_name": request.item_name,
            "category": request.category,
            "tier": request.tier,
            "quick_sell": request.quick_sell
        }

        item = Items(**item_data)
        self.session.add(item)
        await self.session.flush()
        return item

    async def create_item_details(self, item_id: int, request, detail_class: Type):
        details = detail_class(
            item_id=item_id,
            **request.dict(exclude={'item_name', 'category', 'tier', 'quick_sell'})
        )
        self.session.add(details)
        return details

    async def create_item(self, request, detail_class: Type):
        item = await self.create_base_item(request)
        return await self.create_item_details(item.id, request, detail_class)
