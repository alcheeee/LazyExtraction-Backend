from typing import Optional, Union
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from .base_crud import BaseCRUD
from ..models import (
    User,
    Inventory,
    Stats
)


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

    async def get_stats_inv_ids_and_jobname(self, user_id: int):
        query = (
            select(User.stats_id, User.inventory_id, User.job)
            .where(User.id == user_id)
        )
        result = await self.session.execute(query)
        user = result.one_or_none()
        if not user:
            raise Exception("User info not found")
        return user


    async def update_job_stuff(self, inventory_id: int, stats_id: int, update_dict: dict):
        inv_query = select(Inventory.bank, Inventory.energy).where(Inventory.id == inventory_id)
        inv_info = (await self.session.execute(inv_query)).one_or_none()
        if inv_info is None:
            raise Exception("Inventory not found")

        # Calculate new inventory values
        new_bank = inv_info.bank + update_dict['inv_bank']
        new_energy = inv_info.energy - update_dict['inv_energy']
        if new_energy < 0:
            raise ValueError("Not enough energy")

        # Update Inventory table
        inv_update_stmt = update(Inventory).where(
            Inventory.id == inventory_id
        ).values(
            bank=new_bank,
            energy=new_energy
        )
        await self.session.execute(inv_update_stmt)

        # Get current stats values
        stats_query = select(Stats.reputation, Stats.level).where(Stats.id == stats_id)
        stats_info = (await self.session.execute(stats_query)).one_or_none()
        if stats_info is None:
            raise ValueError("Stats not found")

        # Calculate new stats values
        new_rep = stats_info.reputation + update_dict['stats_rep']
        new_level = stats_info.level + update_dict['stats_level']

        # Update Stats table
        stats_update_stmt = update(Stats).where(
            Stats.id == stats_id
        ).values(
            reputation=new_rep,
            level=new_level
        )
        await self.session.execute(stats_update_stmt)

    async def get_stats_education(self, user_id: int):
        user = await self.session.get(
            User, user_id,
            options=[
                selectinload(User.stats),
                selectinload(User.education_progress)
            ]
        )
        return user
