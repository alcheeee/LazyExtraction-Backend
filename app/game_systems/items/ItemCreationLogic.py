from typing import Optional, List
import random
from math import sqrt
from pydantic import BaseModel
from ..gameplay_options import item_quality_mapper, ItemType, ItemQuality


class GenerateItemQuality:
    def __init__(self, user_luck):
        self.user_luck = user_luck

    def generate_item_quality(self) -> ItemQuality:
        qualities = [q.value for q in ItemQuality]
        weights = self.get_luck_weights()
        chosen_quality = random.choices(qualities, weights=weights, k=1)[0]
        return ItemQuality(chosen_quality)

    def get_luck_weights(self) -> [int]:
        quality_settings = {
            ItemQuality.Junk: item_quality_mapper['Junk'],
            ItemQuality.Common: item_quality_mapper['Common'],
            ItemQuality.Uncommon: item_quality_mapper['Uncommon'],
            ItemQuality.Rare: item_quality_mapper['Rare'],
            ItemQuality.Special: item_quality_mapper['Special'],
            ItemQuality.Unique: item_quality_mapper['Unique']
        }
        max_luck_effect = sqrt(self.user_luck)
        adjusted_weights = {
            quality: max(1, int(weight + max_luck_effect * factor))
            for quality, (weight, factor) in quality_settings.items()}

        return [adjusted_weights[q] for q in ItemQuality]


class GenerateItemStats:
    def __init__(self, quality):
        self.quality = quality

    """
    TO BE ADDED
    """


class ItemCreate(BaseModel):
    item_name: str
    quantity: int
    illegal: bool
    category: ItemType
    quality: ItemQuality
    RNG_quality: bool


class WeaponDetailCreate(ItemCreate):
    damage_bonus: int
    evasiveness_bonus: Optional[float]
    strength_bonus: Optional[float]


class ClothingDetailCreate(ItemCreate):
    clothing_type: str
    reputation_bonus: Optional[int]
    max_energy_bonus: Optional[int]
    evasiveness_bonus: Optional[float]
    health_bonus: Optional[int]
    luck_bonus: Optional[float]
    strength_bonus: Optional[float]
    knowledge_bonus: Optional[float]


class IndustrialCraftingCreate(BaseModel):
    item_one: Optional[str]
    item_one_amount: Optional[int]
    item_two: Optional[str]
    item_two_amount: Optional[int]
    item_three: Optional[str]
    item_three_amount: Optional[int]
    produced_item_id: Optional[str]



