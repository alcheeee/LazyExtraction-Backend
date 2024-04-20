from sqlmodel import Session, select
from app.models.models import User
from app.models.other_models import Jobs
from app.database.db import engine
from ..game_systems.gameplay_options import JOB_TYPES
import json
import logging
from app.utils.logger import MyLogger
admin_log = MyLogger.admin()
game_log = MyLogger.game()
user_log = MyLogger.user()


class JobService:

    def get_all_jobs(self, session: Session):
        try:
            query = select(Jobs)
            all_jobs = session.exec(query).all()

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
            session.rollback()
            admin_log.error(str(e))
            return False

    def fetch_user(self, user_id: int, session):
        user = session.get(User, user_id)
        if not user:
            logger.error(f"User {user_id} not found.")
            return None
        return user


    def do_user_job(self, user_id: int, job_name: str):
        with Session(engine) as session:
            transaction = session.begin()
            try:
                user = self.fetch_user(user_id, session)
                job = session.query(Jobs).filter(Jobs.job_name == job_name).first()
                if not job or user.job != job.job_name:
                    admin_log.info(f"Job not found or not assigned to user {user_id}.")
                    raise ValueError("Job not found or not assigned to user.")

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
                session.commit()
                game_log.info(f"{user_id} worked their job!")
                return "Job completed successfully."

            except ValueError as e:
                session.rollback()
                return str(e)
            except Exception as e:
                session.rollback()
                admin_log.error(str(e))
                return False



    def check_qualifications(self, user_id: int, job_name: str):
        with Session(engine) as session:
            user = self.fetch_user(user_id, session)
            job = session.query(Jobs).filter(Jobs.job_name == job_name).first()
            if job:
                required_stats = json.loads(job.required_stats)
                for stat, required_value in required_stats.items():
                    if getattr(user.stats, stat, 0) < required_value:
                        return False
                return True
            return False


    def update_user_job(self, user_id: int, job_name: str):
        with Session(engine) as session:
            transaction = session.begin()
            try:
                user = self.fetch_user(user_id, session)
                if not user:
                    admin_log.error(f"User {user_id} not found.")
                    raise ValueError("User not found.")

                elif job_name == 'quit':
                    user.job = None
                    session.commit()
                    game_log.info(f"User {user_id} quit their job.")
                    return "You quit your job"

                elif self.check_qualifications(user_id, job_name):
                    job = session.query(Jobs).filter(Jobs.job_name == job_name).first()
                    if not job:
                        admin_log.info(f"Job not found. By user {user_id}")
                        raise ValueError("Job not found.")

                    user.job = job.job_name
                    session.commit()
                    game_log.info(f"Updated user {user.id} job to {user.job}.")
                    return f"Congrats! You are now a {job.job_name}!"
                else:
                    game_log.info(f"{user_id} didn't meet the requirements for {job_name}.")
                    raise ValueError("You don't meet the required qualifications.")

            except ValueError as e:
                session.rollback()
                return str(e)

            except Exception as e:
                session.rollback()
                admin_log.error(str(e))
                return False


def create_job(job_data: dict):
    with Session(engine) as session:
        new_job = Jobs(**job_data)
        session.add(new_job)
        session.commit()
        session.refresh(new_job)
        return new_job


job_service = JobService()