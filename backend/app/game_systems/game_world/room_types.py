import random
from typing import List
from functools import lru_cache
from . import WorldNames
from .world_data import room_drops_json


class RoomLootTables:
    def __init__(self, world_name: WorldNames):
        self.base_drops = {
            "regular_room": room_drops_json["regular_room_drops"][world_name],
            "medical_room": room_drops_json["medical_room_drops"][world_name],
            "military_room": room_drops_json["military_room_drops"][world_name]
        }
        self.drop_ranges = {
            WorldNames.Forest: (1, 3),
            WorldNames.Laboratory: (2, 4),
            WorldNames.MilitaryBase: (3, 5)
        }
        self.num_drops_range = self.drop_ranges.get(world_name, (0, 0))

    @lru_cache(maxsize=1000)
    def _prepare_drops(self, room_type: str):
        drops = self.base_drops[room_type]
        return zip(*drops.items())

    def pick_drops(self, room_type: str) -> List[str]:
        items, weights = self._prepare_drops(room_type)
        num_drops = random.randint(*self.num_drops_range)
        return random.choices(items, weights, k=num_drops)

    def regular_room(self):
        return self.pick_drops(self.base_drops["regular_room"])

    def medical_room(self):
        return self.pick_drops(self.base_drops["medical_room"])

    def military_room(self):
        return self.pick_drops(self.base_drops["military_room"])
