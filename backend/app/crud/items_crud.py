from typing import Optional, Any
from sqlalchemy import select
from .base_crud import BaseCRUD
from ..models.item_models import Items


class ItemsCRUD(BaseCRUD):
    async def get_item_from_name(self, item_name: str) -> Items | None:
        query = select(Items).where(
            Items.item_name == item_name  # type: ignore
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_item_field_from_id(
            self, item_id: int, field: str
    ) -> Any | LookupError | None:
        """
        :param item_id: Items.id
        :param field: Table column name 'str'
        :return: Field data
        :raise Exception
        """
        query = select(getattr(Items, field)).where(Items.id == item_id)  # type: ignore
        result = await self.execute_scalar_one_or_none(query)
        if result is None:
            raise LookupError("Item not found")
        return result

    async def check_item_exists(self, name: str):
        """
        :param name: str Items.item_name
        :return: Optional[Items]
        """
        query = select(Items.id).where(Items.item_name == name)  # type: ignore
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_item_name_by_id(self, item_id: int):
        """
        :param item_id: Items.id
        :return: Items.item_name
        :raise Exception
        """
        query = select(Items.item_name).where(
            Items.id == item_id  # type: ignore
        )
        result = await self.execute_scalar_one_or_none(query)
        if result is None:
            raise LookupError("Item not found")
        return result
