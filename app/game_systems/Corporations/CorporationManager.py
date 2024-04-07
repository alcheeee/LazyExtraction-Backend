from sqlmodel import Session, select
from app.models.models import User, Corporations
from app.database.db import engine
import logging
from app.Utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)


class CorporationsManager:
    def __init__(self, engine):
        self.engine = engine

    def check_if_user(self, user_id: int, user):
        with Session(self.engine) as session:
            if user:
                return True
            else:
                logger.error(f"User {user_id} not found.")
                return None

    def create_corporation(self, corp_name: str, corp_type: str, user_id: int):
        with Session(self.engine) as session:

            #Check for existing Corporations
            existing_corporation = session.exec(select(Corporations).where(Corporations.corporation_name == corp_name)).first()
            if existing_corporation:
                logger.error(f"Corporation with name '{corp_name}' already exists.")
                return None

            user = session.get(User, user_id)
            if not self.check_if_user(user_id=user_id, user=user):
                return None

            if user.corp_id:
                logger.info(f"User {user_id} already in a corporation: {user.corp_id}.")
                return None

            #Create corporation in DB if OK
            new_corporation = Corporations(corporation_name=corp_name,
                                           corporation_type=corp_type,
                                           leader=user_id)
            session.add(new_corporation)
            session.commit()

            self.add_user_to_corporation(user_id=user_id, corporation_id = new_corporation.id)
            logger.info(f"New corporation '{corp_name}' created successfully by user {user_id}.")
            return True


    def is_user_in_corporation(self, user_id: int, corporation_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not self.check_if_user(user_id=user_id, user=user):
                return None
            elif user.corp_id == corporation_id:
                logger.info(f"User {user_id} is in that corporation {corporation_id}.")
            else:
                logger.info(f"User {user_id} is not in that corporation {corporation_id}.")


    def add_user_to_corporation(self, user_id: int, corporation_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            corporation = session.get(Corporations, corporation_id)
            if user is None or corporation is None:
                logger.error(f"User {user_id} or Corporation {corporation_id} not found.")
                return None

            elif user.corp_id is None:
                user.corp_id = corporation.id
                session.add(user)
                session.commit()
                logger.info(f"User {user_id} has been added to corporation {corporation_id}.")

            elif user.corp_id == corporation.id:
                logger.info(f"User {user_id} is already in that corporation {corporation_id}.")
            else:
                logger.info(f"User {user_id} is already in corporation {corporation_id}.")


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











