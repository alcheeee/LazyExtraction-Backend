import json
from sqlmodel import Session, select
from typing import Optional, Dict, Type
from app.game_systems.gameplay_options import ItemType, item_bonus_mapper
from app.models.item_models import Items, Weapon, FoodItems
from app.models.models import User, InventoryItem
from app.database.db import engine
from app.utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()
user_log = MyLogger.user()


class ItemStatsHandler:
    def __init__(self, user_id: int, item_id: int):
        self.user_id = user_id
        self.item_id = item_id

    def user_equip_unequip_item(self):
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
                inventory_item = session.query(
                    InventoryItem).filter_by(
                    inventory_id=user.inventory.id,
                    item_id=item.id).first()

                if not inventory_item or inventory_item.quantity == 0:
                    raise ValueError("You do not have that item")

                # Manage currently equipped item
                current_equipped_item = session.query(
                    InventoryItem).filter_by(
                    inventory_id=user.inventory.id,
                    equipped=True).first()

                if current_equipped_item and current_equipped_item.item_id != item.id:
                    current_equipped_item.equipped = False
                    self.adjust_user_stats_item(session, user, current_equipped_item.item, equipping=False)

                inventory_item.equipped = True
                self.adjust_user_stats_item(session, user, item, equipping=True)
                session.commit()

            except Exception as e:
                session.rollback()
                user_log.error(f"User {self.user_id} failed to equip item: {e}")
                return False


    def adjust_user_stats_item(self, session: Session, user, item, equipping=True):
        for stat_key, bonus_attr in item_bonus_mapper.items():
            item_bonus = getattr(item, bonus_attr, 0)
            if item_bonus != 0:
                current_value = getattr(user.stats, stat_key)
                new_value = current_value + (item_bonus if equipping else -item_bonus)
                setattr(user.stats, stat_key, new_value)
        user.stats.round_stats()








