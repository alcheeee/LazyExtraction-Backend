from sqlalchemy import select, update, values, delete
from .BaseCRUD import BaseCRUD
from ..models.item_models import Items
from ..schemas.item_schema import filter_item_stats, ItemType


class ItemsCRUD(BaseCRUD):

    async def get_item_from_id(self, item_id: int):
        return await self.session.get(Items, item_id)

    async def ensure_item_exists_by_id(self, item_id: int):
        query = select(Items.id).where(
            Items.id == item_id
        )
        return await self.execute_scalar_one_or_none(query)

    async def get_item_name_by_id(self, item_id: int):
        query = select(Items.item_name).where(
            Items.id == item_id
        )
        return await self.execute_scalar_one_or_none(query)