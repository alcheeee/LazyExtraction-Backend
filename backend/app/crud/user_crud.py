from typing import Optional, Union, Any, Type
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from .base_crud import BaseCRUD
from ..models import (
    User,
    Inventory,
    Stats
)


class UserCRUD(BaseCRUD):
    async def make_user_admin(self, user_id: int) -> bool:
        update_stmt = update(User).where(User.id == user_id).values(is_admin=True)  # type: ignore
        await self.session.execute(update_stmt)
        return True


    async def get_user_field_from_id(self, user_id: int, field: str) -> Any | None:
        """
        :param user_id: int = User.id
        :param field: User.(field)
        :return: Optional[field]
        """
        query = select(getattr(User, field)).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)

    async def get_user_field_from_username(self, username: str, field: str) -> Any | None:
        """
        :param username: str = User.username
        :param field: User.(field)
        :return: Optional[field]
        """
        query = select(getattr(User, field)).where(User.username == username)
        return await self.execute_scalar_one_or_none(query)

    async def get_user_for_interaction(self, user_id: int) -> User | None:
        query = (
            select(User)
            .options(selectinload(User.stats))
            .where(User.id == user_id)
            .with_for_update()
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_user_id_by_username(self, username: str) -> int | None:
        """
        :param username: str = User.username
        :return: Optional[User.inventory_id]
        """
        query = select(User.id).where(User.username == username)
        return await self.execute_scalar_one_or_none(query)

    async def change_user_crew_id(
            self, username: str, crew_id: int | None = None
    ) -> Union[True, Exception]:
        """
        :param username: str = User.username
        :param crew_id: int = Crew.id
        :return: True
        :raise Exception
        """
        update_stmt = update(User).where(User.username == username).values(crew_id=crew_id)  # type: ignore
        await self.session.execute(update_stmt)
        return True

    async def is_user_admin(self, user_id: int) -> Union[str, False]:
        """
        :param user_id: int = User.id
        :return: username or False
        """
        query = select(User.is_admin, User.username).where(User.id == user_id)  # type: ignore
        result = await self.session.execute(query)
        user_data = result.one_or_none()
        if user_data:
            is_admin, username = user_data
            return username if is_admin else False
        return False

    async def get_stats_inv_ids_and_jobname(self, user_id: int) -> tuple[int, int, str]:
        """
        :param user_id: int = User.id
        :return: (User.stats_id, User.inventory_id, User.job)
        :raise Exception
        """
        query = (
            select(User.stats_id, User.inventory_id, User.job)
            .where(User.id == user_id)  # type: ignore
        )
        result = await self.session.execute(query)
        user = result.one_or_none()
        if not user:
            raise Exception("User info not found")
        return user  # type: ignore

    async def get_stats_education(
            self, user_id: int
    ) -> User | None:
        """
        :param user_id: int = User.id
        :return: (User, User.stats, User.education_progress)
        """
        user = await self.session.get(
            User, user_id,
            options=[
                selectinload(User.stats),  # type: ignore
                selectinload(User.education_progress)
            ]
        )
        return user  # type: ignore
