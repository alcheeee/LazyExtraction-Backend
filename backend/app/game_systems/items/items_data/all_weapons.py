from .. import (
    ItemType,
    ItemTier
)


weapon_items = {
    # Pistols
    'M1911': {
        'item_name': 'M1911',
        'category': ItemType.Weapon,
        'tier': ItemTier.Tier1,
        'quick_sell': 150,
        'weight': 1.1,
        'caliber': '9x19mm',
        'damage': 7,
        'strength': 0.0,
        'range': 50,
        'accuracy': 60,
        'reload_speed': 2.0,
        'fire_rate': 1.2,
        'magazine_size': 7,
        'armor_penetration': 0,
        'headshot_chance': 15,
        'agility_penalty': -0.5,
        'allowed_attachments': {
            "Muzzle": "Flash Suppressor",
            "Magazine": "Extended Magazine",
            "Laser": "Tactical Laser"
        },
        'attachments': {},
    },
    'Beretta M9': {
        'item_name': 'Beretta M9',
        'category': ItemType.Weapon,
        'tier': ItemTier.Tier2,
        'quick_sell': 300,
        'weight': 0.95,
        'caliber': '9x19mm',
        'damage': 8,
        'strength': 0.0,
        'range': 50,
        'accuracy': 65,
        'reload_speed': 1.7,
        'fire_rate': 1.5,
        'magazine_size': 15,
        'armor_penetration': 5,
        'headshot_chance': 18,
        'agility_penalty': -0.3,
        'allowed_attachments': {
            "Muzzle": "Flash Suppressor",
            "Magazine": "Extended Magazine",
            "Laser": "Tactical Laser"
        },
        'attachments': {},
    },

    # Shotguns
    'Sawed-off Shotgun': {
        'item_name': 'Sawed-off Shotgun',
        'category': ItemType.Weapon,
        'tier': ItemTier.Tier1,
        'quick_sell': 200,
        'weight': 2.5,
        'caliber': '12 Gauge',
        'damage': 15,
        'strength': 0.0,
        'range': 20,
        'accuracy': 25,
        'reload_speed': 2.5,
        'fire_rate': 0.8,
        'magazine_size': 2,
        'armor_penetration': 10,
        'headshot_chance': 25,
        'agility_penalty': -1.5,
        'allowed_attachments': {
            "Muzzle": "Flash Suppressor"
        },
        'attachments': {},
    },
    'M890': {
        'item_name': 'M890',
        'category': ItemType.Weapon,
        'tier': ItemTier.Tier2,
        'quick_sell': 400,
        'weight': 3.0,
        'caliber': '12 Gauge',
        'damage': 18,
        'strength': 0.0,
        'range': 30,
        'accuracy': 30,
        'reload_speed': 2.3,
        'fire_rate': 1.0,
        'magazine_size': 6,
        'armor_penetration': 12,
        'headshot_chance': 30,
        'agility_penalty': -1.2,
        'allowed_attachments': {
            "Muzzle": "Flash Suppressor"
        },
        'attachments': {},
    },

    # Assault Rifles
    'M4A1 Carbine': {
        'item_name': 'M4A1 Carbine',
        'category': ItemType.Weapon,
        'tier': ItemTier.Tier3,
        'quick_sell': 1500,
        'weight': 3.1,
        'caliber': '5.56x45mm NATO',
        'damage': 20,
        'strength': 0.0,
        'range': 300,
        'accuracy': 70,
        'reload_speed': 2.0,
        'fire_rate': 3.0,
        'magazine_size': 30,
        'armor_penetration': 20,
        'headshot_chance': 35,
        'agility_penalty': -2.0,
        'allowed_attachments': {
            "Muzzle": "Flash Suppressor",
            "Magazine": "Extended Magazine",
            "Scope": "Sniper Scope",
            "Stock": "Adjustable Stock",
            "Laser": "Tactical Laser"
        },
        'attachments': {},
    },
    'AAC Honey Badger': {
        'item_name': 'AAC Honey Badger',
        'category': ItemType.Weapon,
        'tier': ItemTier.Tier5,
        'quick_sell': 3000,
        'weight': 2.8,
        'caliber': '300 BLK',
        'damage': 25,
        'strength': 0.0,
        'range': 200,
        'accuracy': 75,
        'reload_speed': 1.5,
        'fire_rate': 3.5,
        'magazine_size': 30,
        'armor_penetration': 25,
        'headshot_chance': 40,
        'agility_penalty': -1.5,
        'allowed_attachments': {
            "Muzzle": "Flash Suppressor",
            "Magazine": "Extended Magazine",
            "Scope": "Sniper Scope",
            "Stock": "Adjustable Stock",
            "Laser": "Tactical Laser"
        },
        'attachments': {},
    },
}
