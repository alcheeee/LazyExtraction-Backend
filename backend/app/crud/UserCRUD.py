from typing import Optional, Union
import sqlalchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import select, update
from .BaseCRUD import BaseCRUD
from ..models.models import User, Inventory


class UserCRUD(BaseCRUD):
    async def get_user_field_from_id(self, user_id: int, field: str) -> Optional[object]:
        query = select(getattr(User, field)).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

    async def get_user_inventory_id_by_username(self, username: str) -> Optional[int]:
        """Get user.inventory.id from user.username"""
        query = select(Inventory.id).join(User).where(User.username == username)
        return await self.execute_scalar_one_or_none(query)

    async def change_user_corp_id(self, user_id: int, corp_id: int) -> True or Exception:
        """Change Users corp_id field"""
        update_stmt = update(User).where(User.id == user_id).values(corp_id=corp_id)
        await self.session.execute(update_stmt)
        return True

    async def remove_user_corp_id(self, user_id: int) -> True or Exception:
        """Remove a users corp_id"""
        update_stmt = update(User).where(User.id == user_id).values(corp_id=None)
        await self.session.execute(update_stmt)
        return True

    async def is_user_admin(self, user_id: int) -> Union[str, bool]:
        """Check if user is an admin"""
        query = select(User.is_admin, User.username).where(User.id == user_id)
        result = await self.session.execute(query)
        user_data = result.one_or_none()
        if user_data:
            is_admin, username = user_data
            return username if is_admin else False
        return False
