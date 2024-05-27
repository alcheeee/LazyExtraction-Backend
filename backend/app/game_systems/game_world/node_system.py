import json
from uuid import uuid4
from typing import Dict, Any
from random import randint, choices, sample
from cachetools import cached, TTLCache
from .room_types import RoomLootTables, room_tables
from . import WorldTier, WorldNames

# This will be RNG, rooms will randomly generate options based on a loot table I assign
# Rooms will be assigned based on a room table

cache = TTLCache(maxsize=32, ttl=600)


class NodeSystem:
    def __init__(self, world_name: WorldNames, world_tier: WorldTier = WorldTier.Tier1):
        self.world_name = world_name
        self.world_tier = world_tier
        self.room_types = RoomLootTables(world_name, world_tier)
        self.room_data = room_tables[world_name]
        self.rooms = []

    def _choose_room_type(self) -> str:
        room_names = [room[0] for room in self.room_data['potential_rooms']]
        room_weights = [room[1] for room in self.room_data['potential_rooms']]
        return choices(room_names, room_weights, k=1)[0]

    def _generate_room(self) -> Dict[str, Any]:
        room_type = self._choose_room_type()
        room_items = getattr(self.room_types, room_type)()
        items_with_ids = [{"id": str(uuid4()), "name": item} for item in room_items]
        return {"room_type": room_type, "items": items_with_ids, "connections": []}

    def _create_room_connections(self):
        for room_index, room in enumerate(self.rooms):
            possible_connections = [index for index in range(len(self.rooms)) if index != room_index]
            connections = sample(possible_connections, 1)
            extra_connections = sample(
                [index for index in possible_connections if index not in connections],
                randint(1, 2)
            )
            connections.extend(extra_connections)
            room["connections"] = connections

    def create_node(self):
        num_rooms = randint(*self.room_data['room_amounts'])
        self.rooms = [self._generate_room() for _ in range(num_rooms)]
        self._create_room_connections()

    def to_json(self):
        world = {
            "name": f"{self.world_name.value} - {self.world_tier.value}",
            "rooms": self.rooms
        }
        return json.dumps(world)

    def get_connections(self):
        connections = {}
        for index, room in enumerate(self.rooms):
            connections[index] = room["connections"]
        return connections






