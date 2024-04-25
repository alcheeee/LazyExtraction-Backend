from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Type
from app.game_systems.gameplay_options import ItemType, ItemQuality
from app.game_systems.items.ItemCreationLogic import GenerateItemQuality, GenerateItemStats
from app.models.item_models import Items, Weapon, Clothing
from app.models.models import User
from app.utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()


item_class_map: Dict[ItemType, Type[Items]] = {
    ItemType.Drug: None,     # No class yet
    ItemType.Weapon: Weapon,
    ItemType.Clothing: Clothing,
    ItemType.Other: None     # No class yet
}


async def create_general_item(session: AsyncSession, item_data: dict) -> Items:
    item = Items(**item_data)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def create_item(item_type_str: str, user_id: int, item_details: BaseModel, session: AsyncSession):
    item_class = item_class_map.get(ItemType[item_type_str])
    if not item_class:
        return False, f"No class defined for item type {item_type_str}"

    try:
        user = await session.get(User, user_id)
        if not user:
            return False, "User not found"

        if item_details.RNG_quality:
            user_luck = user.stats.luck
            quality_generator = GenerateItemQuality(user_luck)
            quality = quality_generator.generate_item_quality()
        else:
            quality = item_details.quality

        item_data = {
            "item_name": item_details.item_name,
            "illegal": item_details.illegal,
            "category": ItemType[item_type_str],
            "quality": quality,
            "quantity": item_details.quantity
        }

        if item_details.RNG_quality:
            stats_generator = GenerateItemStats(item_type_str, quality, user.stats.luck)
            additional_details = stats_generator.generate_stats()
        else:
            additional_details = item_details.dict(exclude_unset=True, exclude={
                "item_name","illegal","quality","quantity","RNG_quality","category"})

        if 'clothing_type' not in additional_details and hasattr(item_details, 'clothing_type'):
            additional_details['clothing_type'] = item_details.clothing_type

        item_create = await create_general_item(session, item_data)
        item_detail_instance = item_class(item_id=item_create.id, **additional_details)
        session.add(item_detail_instance)
        await session.commit()
        game_log.info(f"{user_id} created {item_details.item_name}, Quantity: {item_details.quantity}")
        return True, f"Item created successfully."

    except Exception as e:
        raise



