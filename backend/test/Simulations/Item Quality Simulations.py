import pandas as pd
import random
import enum
from math import sqrt
from concurrent.futures import ThreadPoolExecutor


"""
pip uninstall pytz, tzdata, python-dateutil, numpy, pandas

"""

class ItemQuality(enum.Enum):
    Junk = 'Junk'
    Common = 'Common'
    Uncommon = 'Uncommon'
    Rare = 'Rare'
    Special = 'Special'
    Unique = 'Unique'


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
            ItemQuality.Junk: (60, 0.15),
            ItemQuality.Common: (40, 0.1),
            ItemQuality.Uncommon: (35, 0.05),
            ItemQuality.Rare: (10, 1.1),
            ItemQuality.Special: (3, 1.15),
            ItemQuality.Unique: (1, 1.2)
        }
        max_luck_effect = sqrt(self.user_luck)
        adjusted_weights = {
            quality: max(1, int(weight + max_luck_effect * factor))
            for quality, (weight, factor) in quality_settings.items()}

        return [adjusted_weights[q] for q in ItemQuality]


luck_values = range(1, 102, 10)
num_simulations = 100000

results = {luck: {quality: 0 for quality in ItemQuality} for luck in luck_values}

for luck in luck_values:
    generator = GenerateItemQuality(luck)
    for _ in range(num_simulations):
        item_quality = generator.generate_item_quality()
        results[luck][item_quality] += 1

data = {
    quality.value: [((results[luck][quality] / num_simulations) * 100) for luck in luck_values]
    for quality in ItemQuality
}
df = pd.DataFrame(data, index=[f"Luck {luck}" for luck in luck_values])

# Display DataFrame
print(df)
