from .. import (
    ItemType,
    ItemTier
)


bullet_items = {
    '9x19mm': {
        '9x19mm': {
            'item_name': '9x19mm',
            'category': ItemType.Bullets,
            'tier': ItemTier.Tier1,
            'quick_sell': 150,
            'armor_pen_bonus': 0,
            'accuracy_bonus': 0,
            'range_bonus': 0
        },
        '9x19mm AP': {
            'item_name': '9x19mm AP',
            'category': ItemType.Bullets,
            'tier': ItemTier.Tier2,
            'quick_sell': 200,
            'armor_pen_bonus': 5,
            'accuracy_bonus': 0,
            'range_bonus': 5
        },
    },
    '12 Gauge': {
        '12 Gauge': {
            'item_name': '12 Gauge',
            'category': ItemType.Bullets,
            'tier': ItemTier.Tier1,
            'quick_sell': 100,
            'armor_pen_bonus': 0,
            'accuracy_bonus': 0,
            'range_bonus': 0
        },
        '12 Gauge Slug': {
            'item_name': '12 Gauge Slug',
            'category': ItemType.Bullets,
            'tier': ItemTier.Tier2,
            'quick_sell': 150,
            'armor_pen_bonus': 10,
            'accuracy_bonus': 5,
            'range_bonus': 10
        },
    },
    '5.56x45mm NATO': {
        '5.56x45mm NATO': {
            'item_name': '5.56x45mm NATO',
            'category': ItemType.Bullets,
            'tier': ItemTier.Tier2,
            'quick_sell': 300,
            'armor_pen_bonus': 10,
            'accuracy_bonus': 5,
            'range_bonus': 10
        },
        '5.56x45mm NATO AP': {
            'item_name': '5.56x45mm NATO AP',
            'category': ItemType.Bullets,
            'tier': ItemTier.Tier3,
            'quick_sell': 400,
            'armor_pen_bonus': 15,
            'accuracy_bonus': 5,
            'range_bonus': 15
        },
    },
    '300 BLK': {
        '300 BLK': {
            'item_name': '300 BLK',
            'category': ItemType.Bullets,
            'tier': ItemTier.Tier3,
            'quick_sell': 350,
            'armor_pen_bonus': 10,
            'accuracy_bonus': 5,
            'range_bonus': 10
        },
        '300 BLK AP': {
            'item_name': '300 BLK AP',
            'category': ItemType.Bullets,
            'tier': ItemTier.Tier4,
            'quick_sell': 500,
            'armor_pen_bonus': 20,
            'accuracy_bonus': 10,
            'range_bonus': 20
        },
    },
}


