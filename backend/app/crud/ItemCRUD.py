from typing import Optional
from sqlalchemy import select, update, values, delete
from .BaseCRUD import BaseCRUD
from ..models.item_models import Items
from ..schemas.item_schema import filter_item_stats, ItemType


class ItemsCRUD(BaseCRUD):

    async def get_item_field_from_id(self, item_id: int, field: str) -> Optional[object]:
        """
        :param item_id: Items.id
        :param field: Table column name 'str'
        :return: Field data
        :raise Exception
        """
        query = select(getattr(Items, field)).where(Items.id == item_id)
        result = await self.execute_scalar_one_or_none(query)
        if result is None:
            raise Exception("Item not found")
        return result


    async def get_item_from_id(self, item_id: int):
        """
        :param item_id: Items.id
        :return: Items instance
        :raise Exception
        """
        item = await self.session.get(Items, item_id)
        if not item:
            raise Exception("Item not found")
        return item


    async def get_item_name_by_id(self, item_id: int):
        """
        :param item_id: Items.id
        :return: Items.item_name
        :raise Exception
        """
        query = select(Items.item_name).where(
            Items.id == item_id
        )
        result = await self.execute_scalar_one_or_none(query)
        if result is None:
            raise Exception("Item not found")
        return result
