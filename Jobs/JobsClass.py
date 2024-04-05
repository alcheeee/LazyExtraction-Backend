from sqlmodel import Session, select
from models import User, Stats
from db import engine
import logging
from Utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

class Job:
    def __init__(self, job_name: str, job_type: str, income: int, description: str, required_stats: dict, stat_changes: dict):
        self.job_name = job_name
        self.job_type = job_type
        self.income = income
        self.description = description
        self.required_stats = required_stats
        self.stat_changes = stat_changes

    def fetch_user_stats(self, user_id: int, session: Session):
        statement = select(Stats).where(Stats.user_id == user_id)
        results = session.exec(statement)
        user_stats = results.first()
        return user_stats

    def apply_stat_changes(self, user_id: int):
        with Session(engine) as session:
            user_stats = self.fetch_user_stats(user_id, session)
            if not user_stats:
                logger.info("User %s stats not found", user_id)
                return False

            for stat, change in self.stat_changes.items():
                if hasattr(user_stats, stat):
                    setattr(user_stats, stat, getattr(user_stats, stat) + change)

            session.add(user_stats)
            session.commit()
            return True

    def check_qualifications(self, user_id: int):
        with Session(engine) as session:
            user_stats = self.fetch_user_stats(user_id, session)
            if not user_stats:
                logger.info("User %s stats not found", user_id)
                return False

            for stat, required_value in self.required_stats.items():
                if getattr(user_stats, stat, 0) < required_value:
                    return False
            return True



all_jobs = {
    'Store_Bagger': Job(
        job_name='Example Job',
        job_type='General',
        income=100,
        description='Example Description',
        required_stats={'level': 1},
        stat_changes={'energy': -5, 'cash': 200}),

    '': None,
    '': None
}