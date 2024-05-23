from .. import (
    ItemType,
    ItemTier
)

medical_items = {
    'bandage': {
        ItemTier.Tier1: {
            'item_name': 'Gauze',
            'category': ItemType.Medical,
            'tier': ItemTier.Tier1,
            'quick_sell': 6,
            'health_increase': 6
        },
        ItemTier.Tier2: {
            'item_name': 'Compression Bandage',
            'category': ItemType.Medical,
            'tier': ItemTier.Tier2,
            'quick_sell': 10,
            'health_increase': 8
        }
    },
    'pain_killer': {
        ItemTier.Tier1: {
            'item_name': 'Tylopain',
            'category': ItemType.Medical,
            'tier': ItemTier.Tier1,
            'quick_sell': 8,
            'pain_reduction': 6,
            'amount_of_actions': 3
        },
        ItemTier.Tier2: {
            'item_name': 'Morphine',
            'category': ItemType.Medical,
            'tier': ItemTier.Tier2,
            'quick_sell': 12,
            'pain_reduction': 10,
            'amount_of_actions': 1
        },

    },
}


