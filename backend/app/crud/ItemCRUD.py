from sqlalchemy import select, update, values, delete
from .BaseCRUD import BaseCRUD
from ..models.item_models import Items
from ..schemas.item_schema import filter_item_stats, ItemType


class ItemsCRUD(BaseCRUD):

    async def get_item_from_id(self, item_id: int):
        return await self.session.get(Items, item_id)