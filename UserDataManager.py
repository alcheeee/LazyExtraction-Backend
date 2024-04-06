from sqlmodel import Session, select
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

            #Check for name  & email availability
            existing_name = session.exec(select(User).where(User.username == username)).first()
            existing_email = session.exec(select(User).where(User.email == email)).first()
            if existing_name or existing_email:
                logger.error(f"Username {username} or email {email} already exists.")
                return None

            try:
                new_user = User(username=username, password=password, email=email)
                default_stats_data = {
                    'cash': 0,
                    'bank': 1000,
                    'reputation': 0,
                    'education': 'none',
                    'level': 1,
                    'energy': 100,
                    'max_energy': 100,
                    'health': 100,
                    'stamina': 1,
                    'strength': 1,
                    'intelligence': 1,
                    'knowledge': 1}

                user_stats = Stats(**default_stats_data)
                new_user.stats = user_stats
                session.add(new_user)
                session.commit()
                logger.info(f"Created User: {new_user.username}")
                return True

            except Exception as e:
                session.rollback()
                logger.error(f"Failed to create user: {e}")
                return False


    def adjust_energy(self, user_id: int, energy_delta: int):
        with Session(self.engine) as session:
            try:
                user = session.get(User, user_id)
                user_stats = user.stats
            except Exception as e:
                logger.error(f"User {user_id} not found or has no stats. {e}")
                return False

            if user.stats.energy + energy_delta < 0:
                logger.info(f"User {user.id} does not have enough energy.")
                return False

            elif (user.stats.energy + energy_delta) > user.stats.max_energy:
                user.stats.energy = user.stats.max_energy
                session.commit()
                logger.info(f"User {user.id} has max energy.")
                return True

            user.stats.energy += energy_delta
            session.commit()
            logger.info(f"User {user.id}: Energy Adjusted by {energy_delta}. New Energy: {user.stats.energy}.")
            return True


    def update_stat(self, user_id: int, stat_name: str, new_value: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user or not hasattr(user.stats, stat_name):
                logger.error(f"No user found with ID: {user_id} or stat {stat_name}.")
                return False

            setattr(user.stats, stat_name, new_value)
            session.commit()
            logger.info(f"Updated {stat_name} for user: {user.id} to {new_value}.")
            return True

    def update_user_job(self, user_id: int, job_name: str):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user:
                logger.error(f"No user found with ID {user_id}.")
                return False
            user.job = job_name
            session.commit()
            logger.info(f"Updated user {user.id} job: {user.job}.")
            return True

    def get_user_info(self, user_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user:
                logger.error(f"No user found with ID {user_id}.")
                return False
            return user

user_data_manager = UserDataManager(engine)




































