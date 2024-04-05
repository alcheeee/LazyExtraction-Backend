from sqlmodel import Session
from models import User, Stats
from db import engine
import logging
from Utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

class UserDataManager:
    def __init__(self, engine):
        self.engine = engine

    def create_user(self, username: str, password: str, email: str):
        with Session(self.engine) as session:
            try:
                new_user = User(username=username, password=password, email=email)
                default_stats_data = {
                    'cash': 0,
                    'bank': 1000,
                    'education': 'none',
                    'level': 1,
                    'energy': 100,
                    'health': 100,
                    'stamina': 100,
                    'strength': 1,
                    'intelligence': 1,
                    'knowledge': 1}

                user_stats = Stats(**default_stats_data)
                new_user.stats = user_stats
                session.add(new_user)
                session.commit()
                logger.info("Created User: %s", new_user.username)
                return new_user.id

            except Exception as e:
                session.rollback()
                logger.error("Failed to create user: %s", e)
                return False


    def adjust_energy(self, user_id: int, energy_delta: int):
        with Session(self.engine) as session:
            try:
                user = session.get(User, user_id)
                user_stats = user.stats
            except Exception as e:
                logger.error("User %s not found or has no stats. %s", user_id, e)
                return False

            if user.stats.energy + energy_delta < 0:
                logger.info("User %s: does not have enough energy.", user.id)
                return False

            user.stats.energy += energy_delta
            session.commit()
            logger.info("User %s: Energy Adjusted by %s. New Energy: %s", user.id, energy_delta, user.stats.energy)
            return True

    def update_stat(self, user_id: int, stat_name: str, new_value: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user or not hasattr(user.stats, stat_name):
                logger.error("No user found with ID: %s or stat %s", user_id, stat_name)
                return False

            setattr(user.stats, stat_name, new_value)
            session.commit()
            logger.info("Updated %s: for user %s to %s", stat_name, user.id, new_value)
            return True

user_data_manager = UserDataManager(engine)




































