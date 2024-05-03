from sqlalchemy.orm import selectinload
from sqlalchemy import select
from .BaseCRUD import BaseCRUD
from ..models.models import InventoryItem, User


class UserCRUD(BaseCRUD):
    async def check_user_exists(self, user_id: int) -> bool:
        query = select(User.id).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_inventory_item_by_conditions(self, inventory_id, item_id):
        result = await self.session.execute(
            select(InventoryItem)
            .where(
                InventoryItem.inventory_id == inventory_id,
                InventoryItem.item_id == item_id
            )
        )
        return result.scalars().first()

    async def is_user_admin(self, user_id: int):
        query = select(User.is_admin, User.username).where(User.id == user_id)
        result = await self.session.execute(query)
        user_data = result.one_or_none()
        if user_data:
            is_admin, username = user_data
            return username if is_admin else False
        return False

    async def get_user_corp_id(self, user_id: int):
        query = select(User.corp_id).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_username_by_id(self, user_id: int):
        query = select(User.username).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
