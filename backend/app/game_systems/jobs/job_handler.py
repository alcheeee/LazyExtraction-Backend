from app.schemas import JobTypes, JobRequest, JobActionType
from app.database import AsyncSession
from app.crud import JobsCRUD, UserCRUD
from app.models import User, Jobs


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
            JobActionType.Quit: self.quit_job
        }
        if action in action_map:
            result = await action_map[action]()
            return result
        else:
            raise ValueError("Invalid action")

    async def work_job(self):
        user_info = await self.user_crud.get_stats_inv_ids_and_jobname(self.user_id)
        stats_id, inv_id, job_name = user_info

        job = await self.get_job_by_name(job_name)
        if not job:
            raise Exception("No job found")

        update_dict = {
            'stats_rep': job.reputation_adj,
            'stats_level': job.level_adj,
            'inv_bank': job.income,
            'inv_energy': job.energy_required
        }

        await self.job_crud.update_job_stuff(inv_id, stats_id, update_dict)
        return f"Successfully worked job"


    async def quit_job(self):
        await self.job_crud.update_users_job(self.user_id)
        return "You quit your job"


    async def apply_to_job(self):
        job_name = self.request.job_name
        user = await self.user_crud.get_stats_training(self.user_id)
        if user.job:
            raise ValueError("You need to quit your current job first")

        job = await self.get_job_by_name(self.request.job_name)

        if not self.check_qualifications(user, job):
            raise ValueError("You don't meet the required qualifications")

        user.job = job_name
        self.session.add(user)
        return f"Congrats! You are now a {job_name}!"


    async def get_user_job(self):
        user_job = await self.user_crud.get_user_field_from_id(self.user_id, 'job')
        return user_job


    async def get_job_by_name(self, job_name: str):
        job = await self.job_crud.get_job_by_name(job_name)
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





