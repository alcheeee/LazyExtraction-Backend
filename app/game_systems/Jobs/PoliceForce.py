from sqlmodel import Session
from app.models.models import User
from app.database.db import engine
import logging
from app.Utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

class PoliceForce:
    def __init__(self, rank_name: str, income: int, energy_required: int, description: str, required_stats: dict, stat_changes: dict):
        self.rank_name = rank_name
        self.income = income
        self.energy_required = energy_required
        self.description = description
        self.required_stats = required_stats
        self.stat_changes = stat_changes


    def fetch_user_stats(self, user_id: int, session: Session):
        user = session.get(User, user_id)
        user_stats = user.stats
        if not user_stats:
            logger.error(f"User {user_id} stats not found")
            return False
        return user_stats


    def apply_stat_changes(self, user_id: int):
        with Session(engine) as session:
            user_stats = self.fetch_user_stats(user_id, session)
            if user_stats and (user_stats.energy - self.energy_required) >= 0:
                for stat, change in self.stat_changes.items():
                    if hasattr(user_stats, stat):
                        setattr(user_stats, stat, getattr(user_stats, stat) + change)

                user_stats.bank += self.income
                user_stats.energy -= self.energy_required
                session.add(user_stats)
                session.commit()
                return True
            else:
                logger.info(f"User {user_id} doesn't have enough energy")
                return False


    def check_qualifications(self, user_id: int):
        with Session(engine) as session:
            user_stats = self.fetch_user_stats(user_id, session)
            if user_stats:
                for stat, required_value in self.required_stats.items():
                    if getattr(user_stats, stat, 0) < required_value:
                        return False
                return True
            else:
                logger.error(f"User {user_id} stats not found")
                return False



police_ranks = {
    'Volunteer': PoliceForce(
        rank_name='Volunteer',
        income=800,
        energy_required=5,
        description='Fetch paperwork and do errands for the Police.',
        required_stats={'level': 10},
        stat_changes={'strength': 1}),

    '': None,
    '': None
}