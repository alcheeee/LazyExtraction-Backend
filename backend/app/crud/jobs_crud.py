from sqlalchemy import select, update
from .base_crud import BaseCRUD
from ..models import (
    User,
    Jobs
)

class JobsCRUD(BaseCRUD):

    async def check_name_exists(self, name: str):
        """
        :param name: str Jobs.job_name
        :return: Optional[Jobs.job_name]
        """
        query = select(Jobs.job_name).where(Jobs.job_name == name)
        return await self.execute_scalar_one_or_none(query)


    async def get_job_by_name(self, job_name: str):
        """
        :param job_name: str = Jobs.job_name
        :return:
        """
        query = select(Jobs).where(Jobs.job_name == job_name)
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
            .where(User.id == user_id)
            .values(job=job_name)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.session.execute(update_stmt)
        if result.rowcount == 0:
            raise Exception("Failed to update users job")
        return job_name

















