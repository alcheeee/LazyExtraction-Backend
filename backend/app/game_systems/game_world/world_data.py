from . import WorldNames

room_tables = {
    WorldNames.Forest: {
        'potential_rooms': [
            ['medical_room', 15],
            ['regular_room', 65]
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

room_drops_json = {
    "regular_room_drops": {
        WorldNames.Forest: {
            '9x19mm': 50,
            '9x19mm AP': 25,
            '12 Gauge': 30,
            '12 Gauge Slug': 20,
            '5.56x45mm NATO': 10,
            '5.56x45mm NATO AP': 5,
            '300 BLK': 2,
            '300 BLK AP': 1,
            'Stealth Balaclava': 1,
            'Recon Bandana': 0.5,
            'Commando Jacket': 1,
            'Tactical Hoodie': 0.5,
            'Cargo Pants': 1,
            'Stealth Ops Cargo Pants': 0.5
        },
        WorldNames.Laboratory: {
            '9x19mm': 20,
            '9x19mm AP': 10,
            '5.56x45mm NATO': 30,
            '5.56x45mm NATO AP': 15,
            '300 BLK': 10,
            '300 BLK AP': 5,
            'Stealth Balaclava': 0.5,
            'Recon Bandana': 0.3,
            'Commando Jacket': 0.5,
            'Tactical Hoodie': 0.3,
            'Cargo Pants': 0.5,
            'Stealth Ops Cargo Pants': 0.3
        },
        WorldNames.MilitaryBase: {
            '9x19mm': 10,
            '9x19mm AP': 5,
            '5.56x45mm NATO': 40,
            '5.56x45mm NATO AP': 20,
            '300 BLK': 20,
            '300 BLK AP': 10,
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
            '9x19mm': 50,
            '9x19mm AP': 25,
            '12 Gauge': 30,
            '12 Gauge Slug': 20,
            '5.56x45mm NATO': 10,
            '5.56x45mm NATO AP': 5,
            '300 BLK': 2,
            '300 BLK AP': 1,
            'Polymer Rifle Bipod': 2,
            'Tactical Front Grip': 5,
            'Flash Suppressor': 5,
            'Extended Magazine': 3,
            'Adjustable Stock': 4,
            'Sniper Scope': 1,
            'Tactical Laser': 2,
            'Long Barrel': 1,
            'Tactical Helmet': 10,
            'Combat Helmet': 5,
            'Advanced Combat Helmet': 2,
            'Lightweight Vest': 10,
            'Tactical Vest': 5,
            'Heavy Duty Vest': 2
        },
        WorldNames.Laboratory: {
            '9x19mm': 20,
            '9x19mm AP': 10,
            '5.56x45mm NATO': 30,
            '5.56x45mm NATO AP': 15,
            '300 BLK': 10,
            '300 BLK AP': 5,
            'Polymer Rifle Bipod': 3,
            'Tactical Front Grip': 7,
            'Flash Suppressor': 8,
            'Extended Magazine': 6,
            'Adjustable Stock': 7,
            'Sniper Scope': 2,
            'Tactical Laser': 4,
            'Long Barrel': 3,
            'Tactical Helmet': 7,
            'Combat Helmet': 5,
            'Advanced Combat Helmet': 3,
            'Lightweight Vest': 7,
            'Tactical Vest': 5,
            'Heavy Duty Vest': 3
        },
        WorldNames.MilitaryBase: {
            '9x19mm': 10,
            '9x19mm AP': 5,
            '5.56x45mm NATO': 40,
            '5.56x45mm NATO AP': 20,
            '300 BLK': 20,
            '300 BLK AP': 10,
            'Polymer Rifle Bipod': 5,
            'Tactical Front Grip': 10,
            'Flash Suppressor': 10,
            'Extended Magazine': 8,
            'Adjustable Stock': 9,
            'Sniper Scope': 5,
            'Tactical Laser': 7,
            'Long Barrel': 5,
            'Tactical Helmet': 5,
            'Combat Helmet': 3,
            'Advanced Combat Helmet': 2,
            'Lightweight Vest': 5,
            'Tactical Vest': 3,
            'Heavy Duty Vest': 2
        }
    }
}

