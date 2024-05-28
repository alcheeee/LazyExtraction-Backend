from typing import Optional
from sqlalchemy import select
from .base_crud import BaseCRUD
from ..models.item_models import Items


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



    async def check_item_exists(self, name: str):
        """
        :param name: str Items.item_name
        :return: Optional[Items.item_name]
        """
        query = select(Items).where(Items.item_name == name)
        return await self.execute_scalar_one_or_none(query)


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
