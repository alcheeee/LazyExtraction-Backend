from sqlmodel import Session, select
from ..models.models import User, Stats, Inventory
from ..database.db import engine
from ..auth.auth_bearer import pwd_context
import logging
from ..utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

class UserCRUD:
    def __init__(self, engine):
        self.engine = engine

    def create_user(self, username: str, password: str, email: str):
        with Session(self.engine) as session:

            #Check for name  & email availability
            existing_name = session.exec(select(User).where(User.username == username)).first()
            existing_email = session.exec(select(User).where(User.email == email)).first()
            if existing_name or existing_email:
                logger.warning(f"Username {username} or email {email} already exists.")
                msg = f"Username or email already exists."
                return False, msg

            try:
                hashed_password = pwd_context.hash(password)
                new_user = User(username=username, password=hashed_password, email=email)
                default_stats_data = {
                    'reputation': 0,
                    'education': 'none',
                    'level': 1,
                    'max_energy': 100,
                    'health': 100,
                    'stamina': 1,
                    'strength': 1,
                    'intelligence': 1,
                    'knowledge': 1}

                default_inventory_data = {'cash': 0, 'bank': 1000, 'energy': 100}

                new_user.stats = Stats(**default_stats_data)
                new_user.inventory = Inventory(**default_inventory_data)
                session.add(new_user)
                session.commit()
                logger.info(f"Created User: {new_user.username}")
                msg = f"Account created, welcome {username}!"
                return True, msg

            except Exception as e:
                session.rollback()
                logger.error(f"Failed to create user: {e}")
                msg = "Failed to create user."
                return False, msg


    def adjust_energy(self, user_id: int, energy_delta: int):
        with Session(self.engine) as session:
            try:
                user = session.get(User, user_id)

            except Exception as e:
                logger.error(f"User {user_id} not found or has no stats. {e}")
                return False, ""

            user.inventory.energy
            if user.inventory.energy + energy_delta < 0:
                logger.info(f"User {user.id} does not have enough energy.")
                return False, "Not Enough Energy!"

            elif (user.inventory.energy + energy_delta) > user.stats.max_energy:
                user.inventory.energy = user.stats.max_energy
                session.commit()
                logger.info(f"User {user.id} has max energy.")
                return True, "Energy reached max!"

            user.inventory.energy += energy_delta
            session.commit()
            logger.info(f"User {user.id}: Energy Adjusted by {energy_delta}. New Energy: {user.inventory.energy}.")
            return True, str(user.inventory.energy)


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


    def get_user_info(self, user_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user:
                logger.error(f"No user found with ID {user_id}.")
                return False
            return user


    def get_user_by_id(self, user_id: int):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.id == user_id)).first()
            return user


    def get_user_by_username(self, username: str):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.username == username)).first()
            return user


user_crud = UserCRUD(engine)

