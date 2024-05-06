from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from .BaseCRUD import BaseCRUD
from ..models.models import InventoryItem, User


class UserCRUD(BaseCRUD):
    async def check_user_exists(self, user_id: int) -> bool:
        query = select(User.id).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

    async def get_username_by_id(self, user_id: int):
        query = select(User.username).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

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

    # Get Users corp_id field, if any
    async def get_user_corp_id(self, user_id: int):
        query = select(User.corp_id).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

    # Change Users corp_id field
    async def change_user_corp_id(self, user_id: int, corp_id: int):
        update_stmt = update(User).where(User.id == user_id).values(corp_id=corp_id)
        return await self.session.execute(update_stmt)

    # Remove a users corp_id
    async def remove_user_corp_id(self, user_id: int):
        update_stmt = update(User).where(User.id == user_id).values(corp_id=None)
        return await self.session.execute(update_stmt)
