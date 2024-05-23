from .. import (
    ItemType,
    ItemTier
)


armor_items = {
    'Bandage': {
      "item_name": "Helmet",
      "tier": "Tier 1",
      "quick_sell": 10,
      "category": "Weapon",
      "type": "Head",
      "max_durability": 80,
      "current_durability": 100,
      "weight": 5.5,
      "head_protection": 0,
      "chest_protection": 0,
      "stomach_protection": 0,
      "arm_protection": 0,
      "agility_penalty": -0.4
    },
    'Pain Killer': {
        'item_name': 'Pain Killer',
        'tier': ItemTier.Tier1,
        'quick_sell': 12,  # Multiplied by tier
        'category': ItemType.Medical,
        # Multiplied by tier
        'health_increase': 0,
        'pain_reduction': 8,
        'weight_bonus': 0,
        'agility_bonus': 0,
        'amount_of_actions': 3
    },

}
