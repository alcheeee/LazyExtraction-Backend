from sqlmodel import Session, select
from models import User, Corporations
from db import engine
import logging
from Utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)


class CorporationsManager:
    def __init__(self, engine):
        self.engine = engine

    def create_corporation(self, corp_type: str, corp_name: str):
        new_corporation = Corporations(corporation_name=corp_name, corporation_type=corp_type)
        with Session(self.engine) as session:
            session.add(new_corporation)
            session.commit()


    def add_user_to_corporation(self, user_id: int, corporation_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            corporation = session.get(Corporations, corporation_id)
            if user is None or corporation is None:
                logger.info("User %s or Corporation %s not found", user_id, corporation_id)
                return

            user.corp_id = corporation.id
            session.add(user)
            session.commit()
            logger.info("User %s has been added to corporation %s", user.username, corporation.corporation_name)

corporation_manager = CorporationsManager(engine)