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

    item_model_map: Dict[ItemType, Type[BaseModel]] = {
        ItemType.Weapon: Weapon,
        ItemType.Clothing: Clothing,
        ItemType.Drug: None,
        ItemType.Other: None
    }

    def __init__(self, item_details: BaseModel, session: AsyncSession, user_luck=1.0):
        self.item_details = item_details
        self.session = session
        self.user_luck = user_luck

    def get_item_model(self):
        item_model = self.item_model_map.get(self.item_details.category)
        if not item_model:
            raise Exception(f"No class defined for item type {self.item_details.category}")
        return item_model

    def generators(self, quality=None, randomize_all=True):
        if randomize_all:
            quality_generator = GenerateItemQuality(self.user_luck)
            quality = quality_generator.generate_item_quality()

        stats_generator = GenerateItemStats(self.item_details.category, quality, self.user_luck)
        item_specific_details = stats_generator.generate_stats()
        return quality, item_specific_details

    async def create_item(self):
        item_model = self.get_item_model()
        quality = self.item_details.quality

        if self.item_details.randomize_all:
            quality, specific_item_details = self.generators(randomize_all=True)

        elif self.item_details.randomize_stats:
            _, specific_item_details = self.generators(quality=quality, randomize_all=False)

        else:
            specific_item_details = self.item_details.dict(exclude_unset=True, exclude={
                "item_name", "illegal", "quality", "quantity", "randomize_stats", "randomize_all", "category"
            })

        item_data = {
            "item_name": self.item_details.item_name,
            "illegal": self.item_details.illegal,
            "category": self.item_details.category,
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
        return {"item_details": item_data, "specific_details": specific_item_details}