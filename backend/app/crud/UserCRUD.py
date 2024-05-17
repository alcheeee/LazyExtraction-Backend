from typing import Optional, Union
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, update
from .BaseCRUD import BaseCRUD
from ..models.models import User, Inventory


class UserCRUD(BaseCRUD):
    async def get_user_field_from_id(self, user_id: int, field: str) -> Optional[User]:
        """
        :param user_id: int = User.id
        :param field: User.(field)
        :return: Optional[field]
        """
        query = select(getattr(User, field)).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

    async def get_user_inventory_id_by_username(self, username: str) -> Optional[int]:
        """
        :param username: str = User.username
        :return: Optional[User.inventory_id]
        """
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

    async def get_stats_inv_education(self, user_id: int):
        query = (
            select(User)
            .options(
                selectinload(User.stats),
                selectinload(User.education_progress),
                selectinload(User.inventory)
            )
            .where(User.id == user_id)
        )
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise Exception("User stats or Education not found")
        return user


    async def get_stats_education(self, user_id: int):
        user = await self.session.get(
            User, user_id,
            options=[
                selectinload(User.stats),
                selectinload(User.education_progress)
            ]
        )
        return user
