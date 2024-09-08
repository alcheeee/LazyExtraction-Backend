from .. import (
    ItemType,
    ItemTier
)

medical_items = {
    # Bandages
    'Gauze': {
        'item_name': 'Gauze',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier1,
        'quick_sell': 60,
        'health_increase': 6
    },
    'Compression Bandage': {
        'item_name': 'Compression Bandage',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 100,
        'health_increase': 8
    },


    # Pain Killers
    'Tylopain': {
        'item_name': 'Tylopain',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier1,
        'quick_sell': 80,
        'pain_reduction': 6,
        'amount_of_actions': 3
    },
    'Morphine': {
        'item_name': 'Morphine',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 120,
        'pain_reduction': 10,
        'amount_of_actions': 1
    },


    # Stimulant
    'Adrenaline': {
        'item_name': 'Adrenaline',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 200,
        'agility_bonus': 10,
        'strength_bonus': 5,
        'amount_of_actions': 1
    },
    'Ephedrine': {
        'item_name': 'Ephedrine',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier1,
        'quick_sell': 150,
        'agility_bonus': 5,
        'strength_bonus': 3,
        'amount_of_actions': 2
    },


    # First Aid Kits
    'First Aid Kit': {
        'item_name': 'First Aid Kit',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 300,
        'health_increase': 20,
        'pain_reduction': 5,
        'amount_of_actions': 1
    },
    'Advanced First Aid Kit': {
        'item_name': 'Advanced First Aid Kit',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier3,
        'quick_sell': 500,
        'health_increase': 30,
        'pain_reduction': 10,
        'amount_of_actions': 1
    },


    # Injections
    'Steroid Injection': {
        'item_name': 'Steroid Injection',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier3,
        'quick_sell': 400,
        'strength_bonus': 10,
        'agility_bonus': 5,
        'amount_of_actions': 1
    },
    'Pain Relief Injection': {
        'item_name': 'Pain Relief Injection',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 250,
        'pain_reduction': 15,
        'amount_of_actions': 1
    }
}