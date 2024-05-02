from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Type
from .ItemCreationLogic import GenerateItemQuality, GenerateItemStats
from ...crud.ItemCRUD import ItemsCRUD
from ...schemas.item_schema import ItemType, ItemQuality
from ...models.item_models import Items, Weapon, Clothing
from ...models.models import User
from ...utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()

class ItemCreator:

    item_model_map: Dict[ItemType, Type[Items]] = {
        ItemType.Drug: None,
        ItemType.Weapon: Weapon,
        ItemType.Clothing: Clothing,
        ItemType.Other: None
    }

    def __init__(self, item_category, item_details: BaseModel, session: AsyncSession, user_luck=0):
        self.item_category = item_category
        self.item_details = item_details
        self.session = session
        self.user_luck = user_luck

    def get_item_model(self):
        item_model = self.item_model_map.get(ItemType[self.item_category])
        if not item_model:
            raise Exception(f"No class defined for item type {self.item_category}")
        return item_model

    def generators(self):
        quality_generator = GenerateItemQuality(self.user_luck)
        quality = quality_generator.generate_item_quality()
        stats_generator = GenerateItemStats(self.item_category, quality, self.user_luck)
        item_specific_details = stats_generator.generate_stats()
        return quality, item_specific_details

    async def create_item(self):
        item_model = self.get_item_model()
        if self.item_details.randomize_stats:
            quality, specific_item_details = self.generators()
        else:
            quality = self.item_details.quality
            specific_item_details = self.item_details.dict(exclude_unset=True, exclude={
                "item_name", "illegal", "quality", "quantity", "randomize_stats", "category"
            })

        item_data = {
            "item_name": self.item_details.item_name,
            "illegal": self.item_details.illegal,
            "category": ItemType[self.item_category],
            "quality": quality,
            "quantity": self.item_details.quantity
        }

        if 'clothing_type' not in specific_item_details and hasattr(self.item_details, 'clothing_type'):
            specific_item_details['clothing_type'] = self.item_details.clothing_type

        item = Items(**item_data)
        self.session.add(item)
        await self.session.flush()

        item_detail_instance = item_model(item_id=item.id, **specific_item_details)
        self.session.add(item_detail_instance)
        await self.session.commit()
        return f"Item created successfully."




