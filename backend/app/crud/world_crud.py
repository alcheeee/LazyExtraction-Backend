from typing import Optional, Union
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from .base_crud import BaseCRUD
from ..models import (
    User,
    World
)
from ..schemas import WorldCreator


class WorldCRUD(BaseCRUD):

    async def create_node_world(self, world_data: WorldCreator, user: User):
        new_world = World(
            world_tier=world_data.world_tier,
            node_json=world_data.node_json,
            max_players=8,
            players=[user]
        )
        self.session.add(new_world)
        return new_world
