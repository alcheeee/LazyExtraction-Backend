from typing import Optional, List
import random
from math import sqrt
from pydantic import BaseModel
from ..gameplay_options import ItemType, ItemQuality

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

item_quality_mapper = {
    'Junk': (60, 0.15),
    'Common': (40, 0.1),
    'Uncommon': (35, 0.05),
    'Rare': (10, 1.1),
    'Special': (3, 1.15),
    'Unique': (1, 1.2)
}

stat_range_n_boost = {
    # [(min,max), boost]
    ItemQuality.Junk: [(1.0, 4.0), 1],
    ItemQuality.Common: [(1.5, 5.0), 2],
    ItemQuality.Uncommon: [(2.5, 7.0), 4],
    ItemQuality.Rare: [(4.0, 10.0), 5],
    ItemQuality.Special: [(6.0, 14.0), 7],
    ItemQuality.Unique: [(10.0, 18.0), 10]
}


class GenerateItemQuality:
    def __init__(self, luck_stat):
        self.luck_stat = luck_stat

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
        max_luck_effect = sqrt(self.luck_stat)
        adjusted_weights = {
            quality: max(1, int(weight + max_luck_effect * factor))
            for quality, (weight, factor) in quality_settings.items()}

        return [adjusted_weights[q] for q in ItemQuality]


class GenerateItemStats:
    def __init__(self, item_category, quality, luck=None):
        self.category = item_category
        self.quality = quality
        self.luck = luck

    def generate_stats(self):
        relevant_stats = self.get_relevant_stats()
        range_info, boost_chance = stat_range_n_boost[self.quality]

        generated_stats = {}
        if self.category == 'Weapon':
            generated_stats['damage_bonus'] = self.generate_stat_value(range_info)

        num_boosts = random.randint(1, boost_chance + int(self.luck / 10))
        if 'damage_bonus' in generated_stats:
            num_boosts -= 1

        # Don't pick the same stat twice
        additional_stats_to_boost = [stat for stat in relevant_stats if stat not in generated_stats]
        stats_to_boost = random.sample(additional_stats_to_boost, min(num_boosts, len(additional_stats_to_boost)))

        # Generate values randomly for stats
        for stat in stats_to_boost:
            generated_stats[stat] = self.generate_stat_value(range_info)

        return generated_stats


    def generate_stat_value(self, range_info):
        min_range, max_range = range_info
        luck_adjustment = (max_range - min_range) * (self.luck / 100)
        return round(random.uniform(min_range + luck_adjustment, max_range + luck_adjustment), 2)


    def get_relevant_stats(self):
        category_stats = {
            'Weapon': ['damage_bonus', 'evasiveness_bonus', 'strength_bonus'],
            'Clothing': ['reputation_bonus', 'max_energy_bonus', 'evasiveness_bonus',
                         'health_bonus', 'luck_bonus', 'strength_bonus', 'knowledge_bonus']
        }
        return category_stats.get(self.category, [])




