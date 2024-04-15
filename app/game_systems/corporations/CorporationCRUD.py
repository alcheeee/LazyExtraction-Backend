from sqlmodel import Session, select
from app.game_systems.gameplay_options import CORPORATION_TYPES, industrial_corp_defaults, other_corp_defaults
from app.models.models import User, Corporations
from app.database.db import engine
from app.utils.logger import MyLogger
admin_log = MyLogger.admin()
game_log = MyLogger.game()
user_log = MyLogger.user()


class CorporationsManager:
    def __init__(self, engine):
        self.engine = engine

    def create_corporation(self, corp_name: str, corp_type: str, user_id: int):
        with Session(self.engine) as session:
            transaction = session.begin()
            try:
                user = session.get(User, user_id)
                if not user:
                    user_log.error(f"User with ID {user_id} not found when trying to create corporation.")
                    return False, "User not found."

                corp_types = {ctype.value for ctype in CORPORATION_TYPES}
                if corp_type not in corp_types:
                    admin_log.error(f"Invalid corporation type attempted: {corp_type} by {user.username}.")
                    return False, "Invalid Corporation type."

                #Check for existing Corporations
                existing_corporation = session.exec(select(Corporations).where(Corporations.corporation_name == corp_name)).first()
                if existing_corporation:
                    user_log.error(f"Corporation with name '{corp_name}' already exists.")
                    return False, "A corporation with that name already exists."

                if user.corp_id:
                    game_log.info(f"{user.username} attempted to create a new corporation while already in one.")
                    return False, "You must leave your current corporation first!"

                #Create corporation in DB if OK
                new_corporation = Corporations(corporation_name=corp_name, corporation_type=corp_type, leader=user.username)
                new_corporation.corp_inventory = str(industrial_corp_defaults if corp_type == "Industrial" else other_corp_defaults)
                session.add(new_corporation)
                session.commit()
                self.add_user_to_corporation(username=user.username, corporation_id=new_corporation.id)
                game_log.info(f"New corporation '{corp_name}' created successfully by {user.username}.")
                return True, f"{corp_name} created successfully!"

            except Exception as e:
                session.rollback()
                admin_log.error(str(e))
                return False


    def get_corp_from_user(self, user_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user:
                return False
            corporation = session.get(Corporations, user.corp_id)
            return corporation


    def add_user_to_corporation(self, username: str, corporation_id: int):
        with Session(self.engine) as session:
            transaction = session.begin()
            try:
                user = session.exec(select(User).where(User.username == username)).first()
                corporation = session.get(Corporations, corporation_id)
                if user is None or corporation is None:
                    user_log.error(f"User {username} or Corporation {corporation_id} not found.")
                    return None, ""
                elif user.corp_id is None:
                    user.corp_id = corporation.id
                    session.add(user)
                    session.commit()
                    game_log.info(f"{user.username} has been added to corporation {corporation_id}.")
                    return True, f"{user.username} has been added to {corporation.corporation_name}."
                elif user.corp_id == corporation.id:
                    user_log.info(f"{user.username} is already in that corporation {corporation.corporation_name}.")
                    return False, f"{user.username} is already in that corporation {corporation.corporation_name}."
                elif user.corp_id:
                    user_log.info(f"{user.username} is already in a corporation.")
                    return False, f"{user.username} is already in a corporation."

            except Exception as e:
                session.rollback()
                admin_log.error(str(e))
                return False, "Could not add user."


    def remove_user_from_corporation(self, username: int, corporation_id: int):
        with Session(self.engine) as session:
            transaction = session.begin()
            try:
                user = session.exec(select(User).where(User.username == username)).first()
                if user is None or user.corp_id != corporation_id:
                    user_log.error(f"User {username} is not part of corporation {corporation_id}.")
                    return None, "User is not part of that corporation."

                corporation = session.get(Corporations, corporation_id)
                if corporation.leader == user.username:
                    user_log.info(f"User {username} can't leave, leader of corporation {corporation_id}.")
                    return None

                user.corp_id = None
                session.add(user)
                session.commit()
                game_log.info(f"User {username} has been removed from corporation {corporation_id}.")
                return True, f"User removed from {corporation.corporation_name}"
            except Exception as e:
                session.rollback()
                admin_log.error(str(e))
                return False




corporation_manager = CorporationsManager(engine)











