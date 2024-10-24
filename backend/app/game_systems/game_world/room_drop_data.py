from . import WorldNames

room_tables = {
    WorldNames.Forest: {
        'potential_rooms': [
            ['medical_room', 25],
            ['regular_room', 75]
        ]
    },
    WorldNames.Laboratory: {
        'potential_rooms': [
            ['medical_room', 35],
            ['regular_room', 45],
            ['military_room', 20]
        ]
    },
    WorldNames.MilitaryBase: {
        'potential_rooms': [
            ['medical_room', 30],
            ['military_room', 35],
            ['regular_room', 35]
        ]
    }
}

room_loot_tables = {
    "regular_room_drops": {
        WorldNames.Forest: {
            'Stealth Balaclava': 15,
            'Recon Bandana': 0.5,
            'Commando Jacket': 1,
            'Tactical Hoodie': 0.5,
            'Cargo Pants': 1,
            'Stealth Ops Cargo Pants': 0.5
        },
        WorldNames.Laboratory: {
            'Stealth Balaclava': 0.5,
            'Recon Bandana': 0.3,
            'Commando Jacket': 0.5,
            'Tactical Hoodie': 0.3,
            'Cargo Pants': 0.5,
            'Stealth Ops Cargo Pants': 0.3
        },
        WorldNames.MilitaryBase: {
            'Stealth Balaclava': 0.3,
            'Recon Bandana': 0.2,
            'Commando Jacket': 0.3,
            'Tactical Hoodie': 0.2,
            'Cargo Pants': 0.3,
            'Stealth Ops Cargo Pants': 0.2
        },
    },
    "medical_room_drops": {
        WorldNames.Forest: {
            'Gauze': 70,
            'Compression Bandage': 15,
            'Tylopain': 12,
            'Morphine': 6
        },
        WorldNames.Laboratory: {
            'Compression Bandage': 10,
            'Tylopain': 25,
            'Morphine': 14,
            'Ephedrine': 12,
            'Adrenaline': 8
        },
        WorldNames.MilitaryBase: {
            'Compression Bandage': 10,
            'Tylopain': 25,
            'Morphine': 18,
            'Adrenaline': 14,
            'First Aid Kit': 12,
            'Advanced First Aid Kit': 6,
            'Steroid Injection': 6
        }
    },
    "military_room_drops": {
        WorldNames.Forest: {
            'Tactical Short Grip': 5,
            'Flash Suppressor': 5,
            'Extended Magazine': 3,
            'Adjustable Stock': 4,
            'Sniper Scope': 1,
            'Tactical Helmet': 10,
            'Combat Helmet': 5,
            'Advanced Combat Helmet': 2,
            'Lightweight Vest': 10,
            'Tactical Vest': 5,
            'Heavy Duty Vest': 2
        },
        WorldNames.Laboratory: {
            'Tactical Short Grip': 7,
            'Flash Suppressor': 8,
            'Extended Magazine': 6,
            'Adjustable Stock': 7,
            'Sniper Scope': 2,
            'Tactical Helmet': 7,
            'Combat Helmet': 5,
            'Advanced Combat Helmet': 3,
            'Lightweight Vest': 7,
            'Tactical Vest': 5,
            'Heavy Duty Vest': 3
        },
        WorldNames.MilitaryBase: {
            'Tactical Front Grip': 10,
            'Flash Suppressor': 10,
            'Extended Magazine': 8,
            'Adjustable Stock': 9,
            'Sniper Scope': 5,
            'Tactical Helmet': 5,
            'Combat Helmet': 3,
            'Advanced Combat Helmet': 2,
            'Lightweight Vest': 5,
            'Tactical Vest': 3,
            'Heavy Duty Vest': 2
        }
    }
}

