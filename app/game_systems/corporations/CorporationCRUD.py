from sqlmodel import Session, select
from app.game_systems.gameplay_options import CORPORATION_TYPES
from .corp_inventory import CorpDefaults
from app.models.models import User
from app.models.corp_models import Corporations, CorpInventory, CorpInventoryItem
from app.utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()


class CorpManager:
    def __init__(self, session):
        self.session = session
        self.corp_types = {ctype.value for ctype in CORPORATION_TYPES}

    def create_corporation(self, corp_name: str, corp_type: str, user_id: int):
        try:
            user = self.session.get(User, user_id)
            if not user:
                return "User not found."
            if corp_type not in self.corp_types:
                return "Invalid Corporation type."

            existing_corporation = self.session.exec(select(Corporations)
                                                     .where(Corporations.corporation_name == corp_name)).first()
            if existing_corporation:
                return "A corporation with that name already exists."
            if user.corp_id:
                return "You must leave your current corporation first!"

            #Create corporation
            default_inventory = CorpDefaults.get_default_inventory(corp_type).to_dict()
            new_corporation = Corporations(corporation_name=corp_name, corporation_type=corp_type, leader=user.username)
            new_inventory = CorpInventory(corporation=new_corporation)
            self.session.add(new_corporation)
            self.session.add(new_inventory)

            for item_name, quantity in default_inventory.items():
                new_item = CorpInventoryItem(item_name=item_name, quantity=quantity, corp_inventory=new_inventory)
                self.session.add(new_item)

            self.session.commit()
            self.add_user_to_corporation(user.id, new_corporation.id)
            game_log.info(f"New corporation '{corp_name}' created by {user.username}.")
            return f"{corp_name} created successfully!"
        except Exception as e:
            self.session.rollback()
            admin_log.error(e)
            return str(e)


    def add_user_to_corporation(self, user_id: int, corporation_id: int):
        try:
            user = self.session.get(User, user_id)
            corporation = self.session.get(Corporations, corporation_id)
            if user is None or corporation is None:
                return False, "User or Corporation not found"

            if user.corp_id is not None:
                if user.corp_id == corporation.id:
                    return False, f"{user.username} is already in that corporation."
                else:
                    return False, f"{user.username} is already in another corporation."

            user.corp_id = corporation.id
            self.session.commit()
            return True, f"{user.username} has been added to {corporation.corporation_name}."
        except Exception as e:
            self.session.rollback()
            return False, str(e)


    def remove_user_from_corporation(self, user_id: int, corporation_id: int):
        try:
            user = self.session.get(User, user_id)
            if user is None or user.corp_id != corporation_id:
                return False, "User is not part of that corporation"

            corporation = self.session.get(Corporations, corporation_id)
            if corporation.leader == user.username:
                return False, "Leader cannot leave the corporation"

            user.corp_id = None
            self.session.add(user)
            self.session.commit()
            game_log.info(f"User {user_id} has been removed from corporation {corporation_id}.")
            return True, f"User removed from {corporation.corporation_name}"
        except Exception as e:
            self.session.rollback()
            return False, str(e)











