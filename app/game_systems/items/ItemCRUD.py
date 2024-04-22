from pydantic import BaseModel
from sqlmodel import Session
from typing import Dict, Type
from app.game_systems.gameplay_options import ItemType, ItemQuality
from app.game_systems.items.ItemCreationLogic import GenerateItemQuality
from app.models.item_models import Items, Weapon, Clothing
from app.models.models import User
from app.database.db import engine
from app.utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()


item_class_map: Dict[ItemType, Type[Items]] = {
    ItemType.Drug: None,     # No class yet
    ItemType.Weapon: Weapon,
    ItemType.Clothing: Clothing,
    ItemType.Other: None     # No class yet
}


def create_general_item(session: Session, item_data: dict) -> Items:
    item = Items(**item_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def create_item(item_type_str: str, user_id: int, item_details: BaseModel, session: Session):
    item_class = item_class_map.get(ItemType[item_type_str])
    if not item_class:
        return False, f"No class defined for item type {item_type_str}"

    try:
        user = session.get(User, user_id)
        if not user:
            return False, "User not found"

        if item_details.RNG_quality:
            user_luck = user.stats.luck
            generator = GenerateItemQuality(user_luck)
            quality = generator.generate_item_quality()

        item_data = {
            "item_name": item_details.item_name,
            "illegal": item_details.illegal,
            "category": ItemType[item_type_str],
            "quality": item_details.quality,
            "quantity": item_details.quantity
        }

        item_create = create_general_item(session, item_data)
        additional_details = item_details.dict(exclude_unset=True,
                                               exclude={"item_name", "illegal", "quality", "quantity", "RNG_quality"})

        item_detail_instance = item_class(item_id=item_create.id, **additional_details)

        session.add(item_detail_instance)
        session.commit()
        game_log.info(f"{user_id} created {item_details.item_name}, Quantity: {item_details.quantity}")
        return True, f"Item created successfully."

    except Exception as e:
        session.rollback()
        admin_log.error(str(e))
        return False, e



