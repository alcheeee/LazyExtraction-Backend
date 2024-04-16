import json
from sqlmodel import Session, select
from typing import Optional, Dict, Type
from app.game_systems.gameplay_options import ItemType, item_bonus_mapper
from app.models.item_models import Items, Weapon, FoodItems
from app.models.models import User
from app.database.db import engine
from app.utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()
user_log = MyLogger.user()


class ItemStatsHandler:
    def __init__(self, user_id: int, item_id: int):
        self.user_id = user_id
        self.item_id = item_id

    def user_equipped_item(self):
        with Session(engine) as session:
            transaction = session.begin()
            try:

                user = session.get(User, self.user_id)
                item = session.get(Items, self.item_id)

                if not user or not item:
                    raise ValueError("User or item not found")

                if item.category not in ['Clothing', 'Weapon']:
                    raise ValueError("Incorrect item type")

                equipment_map = {
                    "Mask": "equipped_mask",
                    "Body": "equipped_body",
                    "Legs": "equipped_legs",
                    "Weapon": "equipped_weapon"
                }

                item_slot = equipment_map.get(item.category)
                inventory_items = json.loads(user.inventory.inventory_items)
                item_hash = item.hash

                if item_hash not in inventory_items or inventory_items[item_hash]["quantity"] == 0:
                    raise ValueError("You do not have that item")

                if not item_slot:
                    raise ValueError("No valid item slot found for the category")

                current_equipped = getattr(user.inventory, item_slot)
                if current_equipped and int(current_equipped) != item.hash:
                    raise ValueError("You must unequip the current item first")

                if current_equipped:
                    inventory_items[item_hash]["equipped"] = False

                inventory_items[item_hash]["equipped"] = True
                user.inventory.inventory_items = json.dumps(inventory_items)


                setattr(user.inventory, item_slot, item_hash)
                session.commit()


            except Exception as e:
                session.rollback()
                user_log.error(f"User {self.user_id} failed to equip item: {e}")
                return False


    def adjust_user_stats_item(self, session: Session, user, item):
        if item.category == "Weapon":
            user.stats.damage += Weapon.damage
            user.stats.evasiveness += Weapon.evasiveness_bonus
            user.stats.strength += Weapon.strength_bonus

