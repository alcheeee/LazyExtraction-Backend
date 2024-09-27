from sqlalchemy import select, update
from .base_crud import BaseCRUD
from app.models import (
    User,
    Inventory,
    Stats,
    Jobs
)


class JobsCRUD(BaseCRUD):

    async def check_name_exists(self, name: str):
        """
        :param name: str Jobs.job_name
        :return: Optional[Jobs.job_name]
        """
        query = select(Jobs.job_name).where(Jobs.job_name == name)  # type: ignore
        return await self.execute_scalar_one_or_none(query)


    async def get_job_by_name(self, job_name: str):
        """
        :param job_name: str = Jobs.job_name
        :return:
        """
        query = select(Jobs).where(Jobs.job_name == job_name)  # type: ignore
        result = await self.session.execute(query)
        if not result:
            raise Exception("Could not find that job")
        return result.scalars().first()


    async def update_users_job(self, user_id: int, job_name: str = None):
        """
        :param user_id: int = User.id
        :param job_name: str
        :return: str = Job.job_name
        :raise Exception
        """
        update_stmt = (
            update(User)
            .where(User.id == user_id)  # type: ignore
            .values(job=job_name)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.session.execute(update_stmt)
        if result.rowcount == 0:
            raise Exception("Failed to update users job")
        return job_name


    async def update_job_stuff(self, inventory_id: int, stats_id: int, update_dict: dict):
        inv_query = select(
            Inventory.bank, Inventory.energy).where(
            Inventory.id == inventory_id  # type: ignore
        )
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
            Inventory.id == inventory_id  # type: ignore
        ).values(
            bank=new_bank,
            energy=new_energy
        )
        await self.session.execute(inv_update_stmt)

        # Get current stats values
        stats_query = select(
            Stats.reputation, Stats.level).where(
            Stats.id == stats_id  # type: ignore
        )
        stats_info = (await self.session.execute(stats_query)).one_or_none()
        if stats_info is None:
            raise ValueError("Stats not found")

        # Calculate new stats values
        new_rep = stats_info.reputation + update_dict['stats_rep']
        new_level = stats_info.level + update_dict['stats_level']

        # Update Stats table
        stats_update_stmt = update(Stats).where(
            Stats.id == stats_id  # type: ignore
        ).values(
            reputation=new_rep,
            level=new_level
        )
        await self.session.execute(stats_update_stmt)














