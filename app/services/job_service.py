from sqlmodel import select
from app.models.models import User
from app.models.other_models import Jobs
from app.database.db import get_session
from ..game_systems.gameplay_options import JOB_TYPES
import json
import logging
from app.utils.logger import MyLogger
admin_log = MyLogger.admin()
game_log = MyLogger.game()
user_log = MyLogger.user()


class JobService:

    async def get_all_jobs(self, session):
        try:
            all_jobs = (await session.execute(select(Jobs))).scalars().all()
            job_details = []
            for job in all_jobs:
                job_info = {
                    "job_name": job.job_name,
                    "job_type": job.job_type,
                    "income": job.income,
                    "energy_required": job.energy_required,
                    "description": job.description,
                    "required_stats": job.required_stats,
                    "stat_changes": job.stat_changes
                }

                job_details.append(job_info)
            return job_details

        except Exception as e:
            raise


    async def do_user_job(self, user_id: int, job_name: str):
        async with get_session() as session:
            try:
                user = await session.get(User, user_id)
                job = (await session.execute(select(Jobs).where(Jobs.job_name == job_name))).scalars().first()
                if not job or user.job != job.job_name:
                    raise Exception("Job not found or not assigned to user.")

                energy_required = job.energy_required
                if user.inventory.energy < energy_required:
                    raise ValueError("Not enough energy.")

                stat_changes = json.loads(job.stat_changes)
                for stat, change in stat_changes.items():
                    if hasattr(user.stats, stat):
                        setattr(user.stats, stat, getattr(user.stats, stat) + change)

                user.stats.round_stats()
                user.inventory.bank += job.income
                user.inventory.energy -= energy_required
                await session.commit()
                game_log.info(f"{user_id} worked their job!")
                return "Job completed successfully."

            except ValueError as e:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                admin_log.error(str(e))
                raise



    async def check_qualifications(self, user_id: int, job_name: str):
        async with get_session() as session:
            user = await session.get(User, user_id)
            job = (await session.execute(select(Jobs).where(Jobs.job_name == job_name))).scalars().first()
            if job:
                required_stats = json.loads(job.required_stats)
                for stat, required_value in required_stats.items():
                    if getattr(user.stats, stat, 0) < required_value:
                        return False
                return True
            raise Exception("No job found")


    async def update_user_job(self, user_id: int, job_name: str):
        async with get_session() as session:
            try:
                user = await session.get(User, user_id)
                if not user:
                    raise Exception("User not found.")

                elif job_name == 'quit':
                    user.job = None
                    await session.commit()
                    return "You quit your job"

                elif await self.check_qualifications(user_id, job_name):
                    job = (await session.execute(
                        select(Jobs).where(Jobs.job_name == job_name)
                    )).scalars().first()

                    if not job:
                        raise Exception("Job not found.")

                    user.job = job.job_name
                    await session.commit()
                    game_log.info(f"Updated user {user.id} job to {user.job}.")
                    return f"Congrats! You are now a {job.job_name}!"
                else:
                    game_log.info(f"{user_id} didn't meet the requirements for {job_name}.")
                    raise ValueError("You don't meet the required qualifications.")

            except ValueError as e:
                await session.rollback()
                raise

            except Exception as e:
                await session.rollback()
                admin_log.error(f"{str(e)}")
                raise

job_service = JobService()

async def create_job(job_data: dict):
    async with get_session() as session:
        new_job = Jobs(**job_data)
        session.add(new_job)
        await session.commit()
        await session.refresh(new_job)
        return new_job