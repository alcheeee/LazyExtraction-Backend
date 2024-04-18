from sqlmodel import Session, select
from ..models.models import User, Stats, Inventory, InventoryItem
from ..models.item_models import Items
from ..database.db import engine
import bcrypt
import logging
from ..utils.logger import MyLogger
from app.game_systems.gameplay_options import default_stats_data, default_inventory_data, equipment_slots
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()

class UserCRUD:
    def __init__(self, engine):
        self.engine = engine

    def create_user(self, username: str, password: str, email: str):
        with Session(self.engine) as session:
            try:
                #Check for name  & email availability
                existing_user = session.execute(
                    select(User).where((User.username == username) | (User.email == email))
                ).first()

                if existing_user:
                    user_log.warning(f"Username {username} or email {email} already exists.")
                    return False, "Username or email already exists."

                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                new_user = User(username=username, password=hashed_password, email=email)
                new_user.stats = Stats(**default_stats_data)
                new_user.inventory = Inventory(**default_inventory_data)
                session.add(new_user)
                session.commit()
                admin_log.info(f"Created User: {new_user.username}")
                return True, f"Account created, welcome {username}!"

            except Exception as e:
                session.rollback()
                admin_log.error(f"Failed to create user {username}: {str(e)}")
                return False, "Failed to create account due to a server error."


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


    def get_user_by_id(self, user_id: int):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.id == user_id)).first()
            return user


    def get_user_by_username(self, username: str):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.username == username)).first()
            return user


    def update_user_inventory(self, user_id: int, item_id: int, quantity: int = 1, selling=False, session=None):
        user = session.get(User, user_id)
        item = session.get(Items, item_id)
        if not user or not item:
            raise ValueError(f"Couldn't add {item_id} to {user_id}")

        # Get users inventory
        inventory_item = session.query(InventoryItem).filter_by(
            inventory_id=user.inventory.id, item_id=item.id).first()

        if not inventory_item and not selling:
            if quantity <= 0:
                raise ValueError("Cannot add zero or negative quantity.")
            inventory_item = InventoryItem(
                inventory_id=user.inventory.id,
                item_id=item.id,
                quantity=quantity
            )
            session.add(inventory_item)
        else:
            if selling:
                equipped_item_ids = [getattr(user.inventory, slot) for slot in equipment_slots]
                if item.id in equipped_item_ids and inventory_item.quantity <= quantity:
                    raise ValueError("Cannot sell an equipped item.")
                new_quantity = inventory_item.quantity - quantity
            else:
                new_quantity = inventory_item.quantity + quantity

            # Update inventory quantity
            if new_quantity < 0:
                raise ValueError("Not enough items in inventory to remove.")

            if selling and new_quantity < 1 and item.id in equipped_item_ids:
                raise ValueError("Cannot sell all equipped items")
            inventory_item.quantity = new_quantity

        action = "Added" if quantity > 0 else "Removed"
        game_log.info(f"{action} {abs(quantity)} of {item.item_name} to/from {user.username}'s inventory.")
        return True


user_crud = UserCRUD(engine)

