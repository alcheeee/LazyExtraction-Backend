import random
from typing import Dict
from collections import defaultdict
from cachetools import cached, TTLCache
from ...schemas import WorldTier, WorldNames
from ..items.items_data import (
    armor_items,
    valuable_items,
    clothing_items,
    bullet_items,
    medical_items,
    attachment_items,
    weapon_items
)

cache = TTLCache(maxsize=32, ttl=600)

room_tables = {
    WorldNames.Forest: {
        'room_amounts': (10, 16),
        'max_players': 10,
        'potential_rooms': [
            ['medical_room', 15],
            ['regular_room', 65]
        ]
    },
    WorldNames.Laboratory: {
        'room_amounts': (8, 14),
        'max_players': 8,
        'potential_rooms': [
            ['medical_room', 35],
            ['regular_room', 45],
            ['military_room', 20]
        ]
    },
    WorldNames.MilitaryBase: {
        'room_amounts': (14, 18),
        'max_players': 12,
        'potential_rooms': [
            ['medical_room', 30],
            ['military_room', 35],
            ['regular_room', 35]
        ]
    }
}

class RoomLootTables:
    def __init__(self, world_name: WorldNames, room_tier: WorldTier):
        self.world_name = world_name
        self.room_tier = room_tier

    @staticmethod
    def pick_drops(drops: dict, num_drops: int = 1):
        items = list(drops.keys())
        weights = list(drops.values())
        selected_drops = random.choices(items, weights, k=num_drops)
        return selected_drops

    def regular_room(self):
        num_drops = 0
        if self.world_name.Forest:
            num_drops = random.randint(1, 3)
        elif self.world_name.Laboratory:
            num_drops = random.randint(2, 4)
        elif self.world_name.MilitaryBase:
            num_drops = random.randint(3, 5)

        base_drops = self.get_regular_room_drops(self.world_name)
        actual_drops = self.pick_drops(base_drops, num_drops)
        return actual_drops

    @cached(cache)
    def get_regular_room_drops(self, world_name: WorldNames):
        if world_name.Forest:
            return {
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
            }
        elif world_name.Laboratory:
            return {
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
            }
        elif world_name.MilitaryBase:
            return {
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
            }

    def medical_room(self):
        num_drops = 0
        base_drops: Dict[str, float] = {}

        if self.world_name.Forest:
            num_drops = random.randint(1, 2)
            base_drops.update({
                'Gauze': 70,
                'Compression Bandage': 15,
                'Tylopain': 12,
                'Morphine': 6
            })

        elif self.world_name.Laboratory:
            num_drops = random.randint(2, 3)
            base_drops.update({
                'Compression Bandage': 10,
                'Tylopain': 25,
                'Morphine': 14,
                'Ephedrine': 12,
                'Adrenaline': 8
            })

        elif self.world_name.MilitaryBase:
            num_drops = random.randint(2, 4)
            base_drops.update({
                'Compression Bandage': 10,
                'Tylopain': 25,
                'Morphine': 18,
                'Adrenaline': 14,
                'First Aid Kit': 12,
                'Advanced First Aid Kit': 6,
                'Steroid Injection': 6
            })

        actual_drops = self.pick_drops(base_drops, num_drops)
        return actual_drops

    def military_room(self):
        num_drops = 0
        base_drops: Dict[str, float] = {}

        if self.world_name.Forest:
            num_drops = random.randint(1, 3)
            base_drops = {
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
            }

        elif self.world_name.Laboratory:
            num_drops = random.randint(2, 4)
            base_drops = {
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
            }

        elif self.world_name.MilitaryBase:
            num_drops = random.randint(3, 5)
            base_drops = {
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

        actual_drops = self.pick_drops(base_drops, num_drops)
        return actual_drops
