from sqlmodel import Session
from sqlalchemy.orm import joinedload
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

    def fetch_user(self, user_id: int, session):
        user = session.query(User).options(joinedload(User.stats)).filter_by(id=user_id).first()
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
                    return False, "Job not found or not assigned to user."

                energy_required = job.energy_required
                if user.inventory.energy < energy_required:
                    return False, "Not enough energy."

                stat_changes = json.loads(job.stat_changes)
                for stat, change in stat_changes.items():
                    if hasattr(user.stats, stat):
                        setattr(user.stats, stat, getattr(user.stats, stat) + change)

                user.stats.round_stats()
                user.inventory.bank += job.income
                user.inventory.energy -= energy_required
                session.commit()
                game_log.info(f"{user_id} worked their job!")
                return True, "Job completed successfully."

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
                    return False, "User not found."
                elif job_name == 'quit':
                    user.job = None
                    session.commit()
                    game_log.info(f"User {user_id} quit their job.")
                    return True, "You quit your job"
                elif self.check_qualifications(user_id, job_name):
                    job = session.query(Jobs).filter(Jobs.job_name == job_name).first()
                    if not job:
                        admin_log.info(f"Job not found. By user {user_id}")
                        return False, "Job not found."
                    user.job = job.job_name
                    session.commit()
                    game_log.info(f"Updated user {user.id} job to {user.job}.")
                    return True, f"Congrats! You are now a {job.job_name}!"
                else:
                    game_log.info(f"{user_id} didn't meet the requirements for {job_name}.")
                    return False, "You don't meet the required qualifications."

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