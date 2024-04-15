from sqlmodel import Session, select
from ..models.models import User, Stats, Inventory
from ..models.item_models import Items
from ..database.db import engine
import bcrypt
import json
import logging
from ..utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()

class UserCRUD:
    def __init__(self, engine):
        self.engine = engine

    def create_user(self, username: str, password: str, email: str):
        with Session(self.engine) as session:

            #Check for name  & email availability
            existing_name = session.exec(select(User).where(User.username == username)).first()
            existing_email = session.exec(select(User).where(User.email == email)).first()
            if existing_name or existing_email:
                user_log.warning(f"Username {username} or email {email} already exists.")
                msg = f"Username or email already exists."
                return False, msg

            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                new_user = User(username=username, password=hashed_password, email=email)
                new_user.stats = Stats(**default_stats_data)
                new_user.inventory = Inventory(**default_inventory_data)
                session.add(new_user)
                session.commit()
                admin_log.info(f"Created User: {new_user.username}")
                msg = f"Account created, welcome {username}!"
                return True, msg

            except Exception as e:
                session.rollback()
                admin_log.error(f"Failed to create user: {e}")
                msg = "Failed to create user."
                return False, msg


    def adjust_energy(self, user_id: int, energy_delta: int):
        with Session(self.engine) as session:
            transaction = session.begin()
            try:
                user = session.get(User, user_id)
                if not user:
                    admin_log.error(f"User {user_id} not found.")
                    return False, "User not found"


                user.inventory.energy
                if user.inventory.energy + energy_delta < 0:
                    game_log.info(f"User {user.id} does not have enough energy.")
                    return False, "Not Enough Energy!"

                elif (user.inventory.energy + energy_delta) > user.stats.max_energy:
                    user.inventory.energy = user.stats.max_energy
                    session.commit()
                    game_log.info(f"User {user.id} has max energy.")
                    return True, "Energy reached max!"

                user.inventory.energy += energy_delta
                session.commit()
                game_log.info(f"User {user.id}: Energy Adjusted by {energy_delta}. New Energy: {user.inventory.energy}.")
                return True, str(user.inventory.energy)

            except Exception as e:
                session.rollback()
                admin_log.error(str(e))
                return False


    def update_stat(self, user_id: int, stat_name: str, new_value: int):
        with Session(self.engine) as session:
            transaction = session.begin()
            try:
                user = session.get(User, user_id)
                if not user or not hasattr(user.stats, stat_name):
                    admin_log.error(f"No user found with ID: {user_id} or stat {stat_name}.")
                    return False

                setattr(user.stats, stat_name, new_value)
                user.stats.round_stats()
                session.commit()
                game_log.info(f"Updated {stat_name} for user: {user.id} to {new_value}.")
                return True

            except Exception as e:
                session.rollback()
                admin_log.error(str(e))
                return False


    def get_user_by_id(self, user_id: int):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.id == user_id)).first()
            return user


    def get_user_by_username(self, username: str):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.username == username)).first()
            return user


    def add_item_to_user_inventory(self, user_id: int, item_id: int, quantity: int = 1):
        with Session(self.engine) as session:
            transaction = session.begin()
            try:
                user = session.get(User, user_id)
                item = session.exec(select(Items).where(Items.id == item_id)).first()
                if not user or not item:
                    admin_log.error(f"Couldn't get user {user_id} or item {item_id}.")
                    return False, f"Couldn't add {item_id} to {user_id}"

                if item.quantity < quantity:
                    game_log.info(f"REQUESTED {user.id} - Item {item.item_name} has no stock.")
                    return False, f"Item {item.item_name} has no stock."

                inventory_items = json.loads(user.inventory.inventory_items)
                item_id_str = str(item_id)
                inventory_items[item_id_str] = inventory_items.get(item_id_str, 0) + quantity

                item.quantity -= quantity
                user.inventory.inventory_items = json.dumps(inventory_items)

                session.commit()
                game_log.info(f"Added {quantity} of item {item.item_name} to {user.username}'s inventory.")
                return True, f"Added {quantity} {item.item_name} to {user.username}"

            except Exception as e:
                admin_log.error(str(e))
                return False, str(e)


user_crud = UserCRUD(engine)

