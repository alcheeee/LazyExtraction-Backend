from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from ..models.other_models import Jobs
from .BaseCRUD import BaseCRUD

class JobsCRUD(BaseCRUD):
    async def get_by_name(self, name: str):
        query = select(Jobs.job_name).where(Jobs.job_name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, job_data: Jobs):
        try:
            self.session.add(job_data)
            await self.session.commit()
            return job_data
        except Exception as e:
            return None


