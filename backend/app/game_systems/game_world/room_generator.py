import asyncio
from functools import lru_cache
from fastapi.concurrency import run_in_threadpool

import random
from typing import Dict, Any
from itertools import count
from sqlalchemy.ext.asyncio import AsyncSession

from .room_loot_handler import RoomLootTables
from .room_drop_data import room_tables
from . import WorldNames
from . import UserCRUD


class RoomGenerator:
    def __init__(self, world_name: WorldNames):
        self.loot_generator = RoomLootTables(world_name)
        self.world_name = world_name
        self.room_data = room_tables[world_name]
        self.room_id_counter = count()

    @lru_cache(maxsize=100)
    def _get_room_types_and_weights(self):
        return zip(*self.room_data['potential_rooms'])

    def _choose_room_type(self):
        room_names, room_weights = self._get_room_types_and_weights()
        return random.choices(room_names, room_weights, k=1)[0]

    async def generate_room(self) -> Dict[str, Any]:
        room_type = self._choose_room_type()
        room_items = await self.loot_generator.pick_drops(room_type)
        return {
            "room_type": room_type,
            "items": [{"id": next(self.room_id_counter), "name": item} for item in room_items],
            "connections": [next(self.room_id_counter) for _ in range(random.randint(1, 3))]
        }

    async def assign_room_to_user(self, user_id: int, session: AsyncSession):
        user_crud = UserCRUD(None, session)
        user = await user_crud.get_user_for_interaction(user_id)

        if user.in_raid:
            raise ValueError("Already in a raid")

        user.stats.level += 0.1
        user.stats.knowledge += 0.1
        await user.stats.round_stats()

        room_data = await self.generate_room()
        user.current_room_data = room_data
        user.current_world = self.world_name
        user.actions_left = 20
        user.in_raid = True
        return room_data
