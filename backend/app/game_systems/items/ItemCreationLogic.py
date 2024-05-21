import random
from math import sqrt
from typing import List, Dict, Tuple
from ...schemas.item_schema import ItemTier, ItemType, filter_item_stats

class GenerateItemQuality:
    QUALITY_WEIGHTS = {
        ItemTier.Tier1: (60, 1),
        ItemTier.Tier2: (40, 2),
        ItemTier.Tier3: (35, 3),
        ItemTier.Tier4: (10, 4),
        ItemTier.Tier5: (3, 5),
        ItemTier.Tier6: (1, 6)
    }

    def __init__(self, luck_stat):
        self.luck_stat = luck_stat

    def generate_item_quality(self) -> ItemTier:
        qualities = [q for q in ItemTier]
        weights = [self.get_weight(q) for q in qualities]
        quality = random.choices(qualities, weights=weights, k=1)[0]
        return quality

    def get_weight(self, quality: ItemTier) -> int:
        base_weight, luck_factor = self.QUALITY_WEIGHTS[quality]
        luck_effect = sqrt(self.luck_stat) / luck_factor
        return max(1, int(base_weight + luck_effect))

STAT_RANGES: Dict[ItemTier, Tuple[min, max, int]] = {
    ItemTier.Tier1: (1, 3, 1),
    ItemTier.Tier2: (2, 7, 2),
    ItemTier.Tier3: (3, 8, 4),
    ItemTier.Tier4: (6, 14, 5),
    ItemTier.Tier5: (8, 17, 7),
    ItemTier.Tier6: (12, 22, 9)
}

class GenerateItemStats:
    def __init__(self, item_category: ItemType, quality, luck: float):
        self.category = item_category
        self.quality = quality
        self.luck = luck

    def generate_stats(self) -> Dict[str, int]:
        stats = filter_item_stats.get_relevant_stats(self.category)
        generated_stats = {stat: 0 for stat in stats if stat != 'clothing_type'}
        min_range, max_range, num_stats_to_change = STAT_RANGES[self.quality]
        luck_adjustment = sqrt(self.luck)
        stats_picked = 0

        if "damage_bonus" in stats and self.category == ItemType.Weapon:
            generated_stats["damage_bonus"] = self.generate_stat_value(min_range, max_range, luck_adjustment)
            stats_picked += 3 # Arbitrary number, trying to balance damage and other stats
            stats.remove("damage_bonus")

        while stats_picked < num_stats_to_change:
            stat = random.choice(stats)
            stat_addon = self.generate_stat_value(min_range, max_range, luck_adjustment)
            generated_stats[stat] = round(generated_stats[stat] + stat_addon, 2)
            stats_picked += 1

        return generated_stats

    def generate_stat_value(self, min_range, max_range, luck_adjustment) -> float:
        return round(random.uniform(min_range + luck_adjustment, max_range + luck_adjustment), 2)

    def generate_quick_sell(self, quick_sell_value: int):
        quality_multipliers = {
            ItemTier.Tier1: 1,
            ItemTier.Tier2: 2,
            ItemTier.Tier3: 4,
            ItemTier.Tier4: 8,
            ItemTier.Tier5: 16,
            ItemTier.Tier6: 20,
        }
        quick_sell = quick_sell_value * quality_multipliers.get(self.quality, 1)
        return int(quick_sell)






