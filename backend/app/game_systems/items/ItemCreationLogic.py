import random
from math import sqrt
from ...schemas.item_schema import ItemQuality

class GenerateItemQuality:
    QUALITY_WEIGHTS = {
        ItemQuality.Junk: (60, 1),
        ItemQuality.Common: (40, 2),
        ItemQuality.Uncommon: (35, 3),
        ItemQuality.Rare: (10, 4),
        ItemQuality.Special: (3, 5),
        ItemQuality.Unique: (1, 6)
    }

    def __init__(self, luck_stat):
        self.luck_stat = luck_stat

    def generate_item_quality(self) -> ItemQuality:
        qualities = [q for q in ItemQuality]
        weights = [self.get_weight(q) for q in qualities]
        return random.choices(qualities, weights=weights, k=1)[0]

    def get_weight(self, quality: ItemQuality) -> int:
        base_weight, luck_factor = self.QUALITY_WEIGHTS[quality]
        luck_effect = sqrt(self.luck_stat) / luck_factor
        return max(1, int(base_weight + luck_effect))


class GenerateItemStats:
    STAT_RANGES = {
        ItemQuality.Junk: (1, 4),
        ItemQuality.Common: (3, 6),
        ItemQuality.Uncommon: (5, 8),
        ItemQuality.Rare: (7, 10),
        ItemQuality.Special: (9, 12),
        ItemQuality.Unique: (11, 14)
    }

    def __init__(self, item_category, quality, luck=None):
        self.category = item_category
        self.quality = quality
        self.luck = luck

    def generate_stats(self):
        stats = self.get_relevant_stats()
        generated_stats = {}
        min_range, max_range = self.STAT_RANGES[self.quality]
        luck_adjustment = sqrt(self.luck or 0)

        for stat in stats:
            generated_stats[stat] = self.generate_stat_value(min_range, max_range, luck_adjustment)

        return generated_stats

    def generate_stat_value(self, min_range, max_range, luck_adjustment):
        return round(random.uniform(min_range + luck_adjustment, max_range + luck_adjustment), 2)

    def get_relevant_stats(self):
        return {
            'Weapon': ['damage_bonus', 'evasiveness_bonus', 'strength_bonus'],
            'Clothing': ['reputation_bonus', 'max_energy_bonus', 'evasiveness_bonus', 'health_bonus', 'strength_bonus', 'knowledge_bonus']
        }.get(self.category, [])




