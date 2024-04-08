from sqlmodel import Session
from app.models.models import User
from app.database.db import engine
import logging
from app.utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)


class GeneralJob:
    def __init__(self, job_name: str, job_type: str, income: int, energy_required: int, description: str, required_stats: dict, stat_changes: dict):
        self.job_name = job_name
        self.job_type = job_type
        self.income = income
        self.energy_required = energy_required
        self.description = description
        self.required_stats = required_stats
        self.stat_changes = stat_changes


    def fetch_user(self, user_id: int, session: Session):
        user = session.get(User, user_id)
        if not user:
            logger.error(f"User {user_id} not found.")
            return None
        return user


    def do_user_job(self, user_id: int):
        with Session(engine) as session:
            user = self.fetch_user(user_id, session)
            if self.job_name == user.job:
                if user.stats and (user.stats.energy - self.energy_required) >= 0:
                    stat_changes = {}
                    for stat, change in self.stat_changes.items():
                        if hasattr(user.stats, stat):
                            setattr(user.stats, stat, getattr(user.stats, stat) + change)
                            stat_changes[stat] = change

                    user.stats.bank += self.income
                    user.stats.energy -= self.energy_required
                    session.add(user.stats)
                    session.commit()
                    stat_changes['income'] = self.income
                    stat_changes['energy-used'] = self.energy_required
                    return True, f"Stats adjusted: {stat_changes}"
                else:
                    logger.info(f"User {user_id} doesn't have enough energy")
                    return False, "You don't have enough energy."
            else:
                return False, "You don't have that job."


    def check_qualifications(self, user_id: int):
        with Session(engine) as session:
            user = self.fetch_user(user_id, session)
            if user.stats:
                for stat, required_value in self.required_stats.items():
                    if getattr(user.stats, stat, 0) < required_value:
                        return False
                return True
            else:
                logger.error(f"User {user_id} stats not found")
                return False


    def update_user_job(self, user_id: int):
        with Session(engine) as session:
            user = session.get(User, user_id)
            if self.check_qualifications(user.id):
                user.job = self.job_name
                session.commit()
                logger.info(f"Updated user {user.id} job: {user.job}.")
                return True, f"Congrats! You are now a {self.job_name}!"
            else:
                return False, "You don't meet the required qualifications!"