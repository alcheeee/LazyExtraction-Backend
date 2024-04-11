from sqlmodel import Session
from sqlalchemy.orm import joinedload
from app.models.models import User, Jobs
from app.database.db import engine
import json
import logging
from app.utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

JOB_TYPES = ['General', 'Law', 'Crime']

class JobService:

    def fetch_user(self, user_id: int, session):
        user = session.query(User).options(joinedload(User.stats)).filter_by(id=user_id).first()
        if not user:
            logger.error(f"User {user_id} not found.")
            return None
        return user


    def do_user_job(self, user_id: int, job_name: str):
        with Session(engine) as session:
            user = self.fetch_user(user_id, session)
            job = session.query(Jobs).filter(Jobs.job_name == job_name).first()

            if job and user.job == job.job_name:
                energy_required = job.energy_required
                if user.inventory.energy >= energy_required:
                    stat_changes = json.loads(job.stat_changes)
                    for stat, change in stat_changes.items():
                        if hasattr(user.stats, stat):
                            setattr(user.stats, stat, getattr(user.stats, stat) + change)

                    user.stats.round_stats()
                    user.inventory.bank += job.income
                    user.inventory.energy -= energy_required
                    session.commit()
                    return True, "Job completed successfully."
                else:
                    return False, "Not enough energy."
            else:
                return False, "Job not found or not assigned to user."


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
            user = self.fetch_user(user_id, session)
            if not user:
                return False, "User not found."
            elif job_name == 'quit':
                user.job = None
                session.commit()
                return True, "You quit your job"
            elif self.check_qualifications(user_id, job_name):
                job = session.query(Jobs).filter(Jobs.job_name == job_name).first()
                if not job:
                    return False, "Job not found."
                user.job = job.job_name
                session.commit()
                logger.info(f"Updated user {user.id} job to {user.job}.")
                return True, f"Congrats! You are now a {job.job_name}!"
            else:
                return False, "You don't meet the required qualifications."

def create_job(job_data: dict):
    with Session(engine) as session:
        new_job = Jobs(**job_data)
        session.add(new_job)
        session.commit()
        session.refresh(new_job)
        return new_job


job_service = JobService()