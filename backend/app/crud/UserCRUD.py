import sqlalchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import select, update
from .BaseCRUD import BaseCRUD
from ..models.models import User, Inventory


class UserCRUD(BaseCRUD):
    async def get_user_inventory_id_by_username(self, username: str) -> int:
        query = select(Inventory.id).join(User).where(User.username == username)
        return await self.execute_scalar_one_or_none(query)

    async def check_user_exists(self, user_id: int) -> int or None:
        query = select(User.id).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

    async def get_username_by_id(self, user_id: int) -> str or None:
        query = select(User.username).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

    async def is_user_admin(self, user_id: int) -> str or False:
        query = select(User.is_admin, User.username).where(User.id == user_id)
        result = await self.session.execute(query)
        user_data = result.one_or_none()
        if user_data:
            is_admin, username = user_data
            return username if is_admin else False
        return False

    async def get_user_inventory_id(self, user_id: int) -> int or None:
        query = select(User.inventory.id).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

    # Get Users corp_id field, if any
    async def get_user_corp_id(self, user_id: int) -> int or None:
        query = select(User.corp_id).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

    # Change Users corp_id field
    async def change_user_corp_id(self, user_id: int, corp_id: int) -> True or Exception:
        update_stmt = update(User).where(User.id == user_id).values(corp_id=corp_id)
        return await self.session.execute(update_stmt)

    # Remove a users corp_id
    async def remove_user_corp_id(self, user_id: int) -> True or Exception:
        update_stmt = update(User).where(User.id == user_id).values(corp_id=None)
        return await self.session.execute(update_stmt)
