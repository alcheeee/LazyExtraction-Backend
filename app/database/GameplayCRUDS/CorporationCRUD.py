from sqlmodel import Session, select
from app.models.models import User, Corporations
from app.database.db import engine
import logging
from app.utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

CORPORATION_TYPES = ['Industrial', 'Law', 'Restaurant', 'Criminal']

class CorporationsManager:
    def __init__(self, engine):
        self.engine = engine

    def create_corporation(self, corp_name: str, corp_type: str, user_id: int):
        with Session(self.engine) as session:

            user = session.get(User, user_id)
            if not user:
                return None, ""

            if corp_type not in CORPORATION_TYPES:
                return False, "Invalid Corporation type."

            #Check for existing Corporations
            existing_corporation = session.exec(select(Corporations).where(Corporations.corporation_name == corp_name)).first()
            if existing_corporation:
                logger.error(f"Corporation with name '{corp_name}' already exists.")
                return False, "A corporation with that name already exists."

            if user.corp_id:
                logger.info(f"{user.username} already in a corporation: {user.corp_id}.")
                return False, "You must leave your corporation first!"

            #Create corporation in DB if OK
            new_corporation = Corporations(corporation_name=corp_name,
                                           corporation_type=corp_type,
                                           leader=user.username)
            session.add(new_corporation)
            session.commit()

            self.add_user_to_corporation(username=user.username, corporation_id = new_corporation.id)
            logger.info(f"New corporation '{corp_name}' created successfully by {user.username}.")
            return True, f"{corp_name} created successfully!"


    def is_user_in_corporation(self, user_id: int, corporation_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user:
                return None, ""
            elif user.corp_id == corporation_id:
                logger.info(f"User {user_id} is in that corporation {corporation_id}.")
                return True, ""
            else:
                logger.info(f"User {user_id} is not in that corporation {corporation_id}.")
                return False, ""


    def is_user_leader(self, user_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            corporation = session.get(Corporations, user.corp_id)
            if user.username == corporation.leader:
                return True
            else:
                return False


    def get_corp_from_user(self, user_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user:
                return False
            corporation = session.get(Corporations, user.corp_id)
            return corporation


    def add_user_to_corporation(self, username: int, corporation_id: int):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.username == username)).first()
            corporation = session.get(Corporations, corporation_id)

            if user is None or corporation is None:
                logger.error(f"User {username} or Corporation {corporation_id} not found.")
                return None, ""

            elif user.corp_id is None:
                user.corp_id = corporation.id
                session.add(user)
                session.commit()
                logger.info(f"{user.username} has been added to corporation {corporation_id}.")
                return True, f"{user.username} has been added to {corporation.corporation_name}."

            elif user.corp_id == corporation.id:
                logger.info(f"{user.username} is already in that corporation {corporation.corporation_name}.")
                return False, f"{user.username} is already in that corporation {corporation.corporation_name}."
            else:
                return False, ""


    def remove_user_from_corporation(self, user_id: int, corporation_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if user is None or user.corp_id != corporation_id:
                logger.error(f"User {user_id} is not part of corporation {corporation_id}.")
                return None

            corporation = session.get(Corporations, corporation_id)
            if corporation.leader == user.id:
                logger.info(f"User {user_id} can't leave, leader of corporation {corporation_id}.")
                return None

            user.corp_id = None
            session.add(user)
            session.commit()
            logger.info(f"User {user_id} has been removed from corporation {corporation_id}.")





corporation_manager = CorporationsManager(engine)










