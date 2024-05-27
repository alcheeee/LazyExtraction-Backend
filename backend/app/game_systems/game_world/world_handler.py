from uuid import uuid4
from random import choices, randint
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from ...crud import UserCRUD, WorldCRUD
from . import (
    WorldCreator,
    WorldNames,
    WorldTier
)
from .node_system import NodeSystem
from .room_types import RoomLootTables, room_tables


class RoomGenerator:
    def __init__(self, world_name: WorldNames, world_tier: WorldTier = WorldTier.Tier1):
        self.world_name = world_name
        self.world_tier = world_tier
        self.room_types = RoomLootTables(world_name, world_tier)
        self.room_data = room_tables[world_name]

    def _choose_room_type(self) -> str:
        room_names = [room[0] for room in self.room_data['potential_rooms']]
        room_weights = [room[1] for room in self.room_data['potential_rooms']]
        return choices(room_names, room_weights, k=1)[0]

    def _generate_room(self) -> Dict[str, Any]:
        room_id = str(uuid4())
        room_type = self._choose_room_type()
        room_items = getattr(self.room_types, room_type)()
        items_with_ids = [{"id": str(uuid4()), "name": item} for item in room_items]
        connections = [str(uuid4()) for _ in range(randint(1, 3))]  # Generate between 1 and 3 next rooms
        return {"id": room_id, "room_type": room_type, "items": items_with_ids, "connections": connections}

    def generate_next_room(self) -> Dict[str, Any]:
        return self._generate_room()



class CreateNodeWorld:
    def __init__(self, world_data: WorldCreator, user_id: int, session: AsyncSession):
        self.world_data = world_data
        self.user_id = user_id
        self.session = session
        self.user_crud = UserCRUD(None, session)
        self.world_crud = WorldCRUD(None, session)

    async def create_world(self):
        user = await self.user_crud.get_user(self.user_id)

        #if user.in_raid:
        #    raise ValueError("Already in a raid")

        node_system = NodeSystem(self.world_data.world_name, self.world_data.world_tier)
        node_system.create_node()
        node_json = node_system.to_json()

        new_world_data = WorldCreator(
            world_name=self.world_data.world_name,
            world_tier=self.world_data.world_tier,
            node_json=node_json
        )

        new_world = await self.world_crud.create_node_world(new_world_data, user)
        user.in_raid = True
        return new_world




