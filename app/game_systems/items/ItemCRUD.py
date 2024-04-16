import datetime
import hashlib
import time

from sqlmodel import Session
from typing import Optional, Dict, Type
from app.game_systems.gameplay_options import ItemType, ItemQuality, item_quality_mapper
from app.game_systems.items.ItemCreationLogic import GenerateItemQuality
from app.models.item_models import Items, Weapon, FoodItems, Clothing
from app.models.models import User
from app.database.db import engine
from app.config import settings
from app.utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()


item_class_map: Dict[ItemType, Type[Items]] = {
    ItemType.Food: FoodItems,
    ItemType.Drug: None,     # No class yet
    ItemType.Weapon: Weapon,
    ItemType.Clothing: Clothing,
    ItemType.Other: None     # No class yet
}


def is_item_type(item_type_str):
    try:
        item_type = ItemType(item_type_str)
        return True
    except ValueError:
        return False


def item_data_json(item_name: str, illegal: bool, category: str,
                   random_generate_quality: bool, quality: str,
                   quantity: int, user_luck):

    if random_generate_quality:
        generator = GenerateItemQuality(user_luck=user_luck)
        quality = generator.generate_item_quality()

    item_data = {
         "item_name": item_name,
         "illegal": illegal,
         "category": category,
         "quality": quality,
         "quantity": quantity,
         "hash": None
        }

    return item_data


def generate_hash(item_id):
    unique_string = f"{item_id}-{time.time()}-{settings.ITEMS_SECRET_KEY}"
    return hashlib.sha224(unique_string.encode()).hexdigest()

def create_general_item(session: Session, item_data: dict) -> Items:
    item = Items(**item_data)
    session.add(item)
    session.commit()
    item.hash = generate_hash(item.id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def create_item(item_type_str: str, user_id: int, item_details,
                item_name: str, illegal: bool, random_generate_quality: bool,
                quality: ItemQuality, quantity: int):

    if not is_item_type(item_type_str):
        game_log.error(f"Invalid item type attempted: {item_type_str}")
        return False, "Not a valid item type."

    item_type_enum = ItemType[item_type_str]
    item_class = item_class_map.get(item_type_enum)

    if not item_class:
        game_log.error(f"No class defined for item type {item_type_str}")
        return False, {"message": f"No class defined for item type {item_type_str}"}

    with Session(engine) as session:
        transaction = session.begin()
        try:
            user = session.get(User, user_id)
            if not user:
                game_log.error(f"User not found: User ID {user_id}")
                return False, "User not found"

            user_luck = user.stats.luck
            item_data = item_data_json(item_name, illegal, item_type_enum, random_generate_quality, quality, quantity, user_luck)
            item_create = create_general_item(session, item_data)
            item_detail = item_class(item_id=item_create.id, **item_details.dict())
            session.add(item_detail)
            session.commit()
            game_log.info(f"{user_id} created {item_name}, Quantity: {quantity}")
            return True, {"message": f"Item created successfully.", "item_name": item_name}

        except Exception as e:
            session.rollback()
            admin_log.error(str(e))
            return False, {"message": "Error creating item"}
