import random
from math import sqrt
from typing import List, Dict, Tuple
from ...schemas.item_schema import ItemQuality, ItemType, filter_item_stats

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

STAT_RANGES: Dict[ItemQuality, Tuple[int, int, int]] = {
    ItemQuality.Junk: (1, 3, 1),
    ItemQuality.Common: (2, 7, 2),
    ItemQuality.Uncommon: (3, 8, 4),
    ItemQuality.Rare: (6, 14, 5),
    ItemQuality.Special: (8, 17, 7),
    ItemQuality.Unique: (12, 22, 9)
}

class GenerateItemStats:
    def __init__(self, item_category: ItemType, quality, luck: float):
        self.category = item_category
        self.quality = quality
        self.luck = luck

    def generate_stats(self) -> Dict[str, int]:
        stats = filter_item_stats.get_relevant_stats(self.category)
        generated_stats = {stat: 0 for stat in stats}
        min_range, max_range, num_stats_to_change = STAT_RANGES[self.quality]
        luck_adjustment = sqrt(self.luck)
        stats_picked = 0

        if "damage_bonus" in stats and self.category == ItemType.Weapon:
            generated_stats["damage_bonus"] = self.generate_stat_value(min_range, max_range, luck_adjustment)
            stats_picked += 3
            stats.remove("damage_bonus")

        while stats_picked < num_stats_to_change:
            stat = random.choice(stats)
            stat_addon = self.generate_stat_value(min_range, max_range, luck_adjustment)
            generated_stats[stat] = round(generated_stats[stat] + stat_addon, 2)
            stats_picked += 1

        return generated_stats

    def generate_stat_value(self, min_range, max_range, luck_adjustment) -> float:
        return round(random.uniform(min_range + luck_adjustment, max_range + luck_adjustment), 2)


