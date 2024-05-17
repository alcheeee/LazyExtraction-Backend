from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from ...models.models import User
from ...models.other_models import Jobs
from ...schemas.job_schema import JobTypes, JobRequest, JobActionType
from ...crud.JobsCRUD import JobsCRUD
from ...crud.UserCRUD import UserCRUD
import json
import logging
from ...utils import MyLogger
user_log = MyLogger.user()


class JobService:

    def __init__(self, request: JobRequest, user_id: int, session: AsyncSession):
        self.request = request
        self.user_id = user_id
        self.session = session
        self.job_crud = JobsCRUD(Jobs, session)
        self.user_crud = UserCRUD(User, session)


    async def handle_job_action(self):
        action = self.request.job_action
        action_map = {
            JobActionType.Work: self.work_job,
            JobActionType.Apply: self.apply_to_job,
            JobActionType.Quit: self.quit_job,
            JobActionType.AskForPromo: self.ask_for_promotion
        }
        if action in action_map:
            result = await action_map[action]()
            return result
        else:
            raise ValueError("Invalid action")


    async def work_job(self):
        return "Test complete"


    async def quit_job(self):
        pass


    async def apply_to_job(self):
        job_name = self.request.job_name
        user = await self.user_crud.get_stats_education(self.user_id)
        if user.job:
            raise ValueError("You need to quit your current job first")

        job = await self.get_job_by_name()

        if not self.check_qualifications(user, job):
            raise ValueError("You don't meet the required qualifications")

        user.job = job_name
        self.session.add(user)
        return f"Congrats! You are now a {job_name}!"


    async def ask_for_promotion(self):
        pass


    async def get_user_job(self):
        user_job = await self.user_crud.get_user_field_from_id(self.user_id, 'job')
        return user_job


    async def get_job_by_name(self):
        job = await self.job_crud.get_job_by_name(self.request.job_name)
        if not job:
            raise Exception("Job not found")
        return job


    @staticmethod
    def check_qualifications(user, job: Jobs = None):
        if user.stats.level < job.level_required:
            return False
        if user.stats.reputation < job.reputation_required:
            return False
        if job.education_required and user.education_progress is None:
            return False
        if not job.education_required:
            return True

        education_progress_field = getattr(user.education_progress, job.education_required, 0)
        if education_progress_field < job.education_progress_required:
            return False
        return True





