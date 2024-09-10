import asyncio
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

from random import randint, choices
from typing import Dict, Any
from itertools import count
from sqlalchemy.ext.asyncio import AsyncSession

from .room_types import RoomLootTables
from .world_data import room_tables
from . import WorldNames
from . import UserCRUD
from . import RetryDecorators


class RoomGenerator:
    def __init__(self, world_name: WorldNames):
        self.loot_generator = RoomLootTables(world_name)
        self.world_name = world_name
        self.room_data = room_tables[world_name]
        self.room_id_counter = count()
        self.executor = ThreadPoolExecutor()

    @lru_cache(maxsize=100)
    def _get_room_types_and_weights(self):
        return zip(*self.room_data['potential_rooms'])

    def _choose_room_type(self):
        room_names, room_weights = self._get_room_types_and_weights()
        return choices(room_names, room_weights, k=1)[0]

    def _generate_room_sync(self) -> Dict[str, Any]:
        room_type = self._choose_room_type()
        room_items = self.loot_generator.pick_drops(room_type)
        connections = [next(self.room_id_counter) for _ in range(randint(1, 3))]

        return {
            "room_type": room_type,
            "items": [{"id": next(self.room_id_counter), "name": item} for item in room_items],
            "connections": connections
        }

    async def generate_room(self) -> Dict[str, Any]:
        loop = asyncio.get_running_loop()
        room_data = await loop.run_in_executor(self.executor, self._generate_room_sync)
        return room_data

    async def assign_room_to_user(self, user_id: int, session: AsyncSession):
        try:
            user_crud = UserCRUD(None, session)
            user = await user_crud.get_user_for_interaction(user_id)

            if user.in_raid:
                raise ValueError("Already in a raid")

            user.stats.level += 0.1
            user.stats.knowledge += 0.1
            user.stats.round_stats()

            room_data = await self.generate_room()
            user.current_room_data = room_data
            user.current_world = self.world_name
            user.actions_left = 20
            user.in_raid = True
            return room_data

        except Exception as e:
            raise Exception(f"Unexpected error in assign_room_to_user: {e}")
