from .. import (
    ItemType,
    ItemTier,
    ArmorType
)

armor_items = {
    # Head Armor
    'Tactical Helmet': {
        'item_name': 'Tactical Helmet',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier1,
        'quick_sell': 500,
        'type': ArmorType.Head,
        'weight': 1.5,
        'head_protection': 15,
        'chest_protection': 0,
        'stomach_protection': 0,
        'arm_protection': 0,
        'agility_penalty': -0.1
    },
    'Combat Helmet': {
        'item_name': 'Combat Helmet',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier2,
        'quick_sell': 1000,
        'type': ArmorType.Head,
        'weight': 2.0,
        'head_protection': 25,
        'chest_protection': 0,
        'stomach_protection': 0,
        'arm_protection': 0,
        'agility_penalty': -0.15
    },
    'Advanced Combat Helmet': {
        'item_name': 'Advanced Combat Helmet',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier3,
        'quick_sell': 2000,
        'type': ArmorType.Head,
        'weight': 2.5,
        'head_protection': 35,
        'chest_protection': 0,
        'stomach_protection': 0,
        'arm_protection': 0,
        'agility_penalty': -0.2
    },

    # Body Armor
    'Lightweight Vest': {
        'item_name': 'Lightweight Vest',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier1,
        'quick_sell': 750,
        'type': ArmorType.Body,
        'weight': 3.0,
        'head_protection': 0,
        'chest_protection': 20,
        'stomach_protection': 10,
        'arm_protection': 5,
        'agility_penalty': -0.2
    },
    'Tactical Vest': {
        'item_name': 'Tactical Vest',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier2,
        'quick_sell': 1500,
        'type': ArmorType.Body,
        'weight': 4.0,
        'head_protection': 0,
        'chest_protection': 30,
        'stomach_protection': 20,
        'arm_protection': 10,
        'agility_penalty': -0.3
    },
    'Heavy Duty Vest': {
        'item_name': 'Heavy Duty Vest',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier3,
        'quick_sell': 2500,
        'type': ArmorType.Body,
        'weight': 5.0,
        'head_protection': 0,
        'chest_protection': 40,
        'stomach_protection': 30,
        'arm_protection': 15,
        'agility_penalty': -0.4
    }
}
