from sqlmodel import Session
from typing import Optional, Dict, Type
from app.game_systems.gameplay_options import ItemType, ItemQuality, item_quality_mapper
from app.game_systems.items.ItemCreationLogic import GenerateItemQuality
from app.models.item_models import Items, Weapon, FoodItems, IndustrialCraftingRecipes
from app.models.models import User
from app.database.db import engine


item_class_map: Dict[ItemType, Type[Items]] = {
    ItemType.Food: FoodItems,
    ItemType.IndustrialCrafting: IndustrialCraftingRecipes,
    ItemType.Drug: None,     # No class yet
    ItemType.Weapon: Weapon,
    ItemType.Clothing: None, # No class yet
    ItemType.Other: None     # No class yet
}


def is_item_type(item_type_str):
    try:
        item_type = ItemType(item_type_str)
        return True
    except ValueError:
        return False

def item_data_json(item_name: str, illegal: bool, buy_price: int, category: str,
                   random_generate_quality: bool, quality: str, quantity: int, user_luck):
    if random_generate_quality:
        generator = GenerateItemQuality(user_luck=user_luck)
        quality = generator.generate_item_quality()

    item_data = {
         "item_name": item_name,
         "illegal": illegal,
         "buy_price": buy_price,
         "category": category,
         "quality": quality,
         "quantity": quantity
        }

    return item_data


def create_general_item(session: Session, item_data: dict) -> Items:
    item = Items(**item_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def create_item(item_type_str: str, user_id: int, item_details,
                item_name: str, illegal: bool, random_generate_quality: bool,
                quality: ItemQuality, quantity: int, buy_price: int):

    if not is_item_type(item_type_str):
        return False, "Not a valid item type."

    item_type_enum = ItemType[item_type_str]
    item_class = item_class_map.get(item_type_enum)

    if not item_class:
        return False, f"No class defined for item type {item_type_str}"

    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            return False, "User not found"

        user_luck = user.stats.luck
        item_data = item_data_json(item_name, illegal, buy_price, item_type_enum, random_generate_quality, quality, quantity, user_luck)
        item_create = create_general_item(session, item_data)
        item_detail = item_class(item_id=item_create.id, **item_details.dict())
        session.add(item_detail)
        session.commit()
        return True, {"message": f"Item created successfully.", "item_name": item_name}
