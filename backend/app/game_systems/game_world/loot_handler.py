from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from ...crud import UserCRUD, WorldCRUD
from ...schemas import RoomInteraction, WorldTier
from .world_handler import RoomGenerator



class InteractionHandler:
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id
        self.user_crud = UserCRUD(None, session)

    async def get_user(self):
        return await self.user_crud.get_user(self.user_id)

    async def update_current_room_data(self, new_room_data: dict):
        user = await self.get_user()
        user.current_room_data = new_room_data
        await self.session.commit()
        await self.session.refresh(user)
        return user.current_room_data


    async def item_pickup(self, item_id: UUID4):
        user = await self.get_user()
        current_room_data = user.current_room_data

        item = next((item for item in current_room_data["items"] if item["id"] == str(item_id)), None)
        if item:
            current_room_data["items"].remove(item)
            # Add item to user's inventory here (pseudo-code)
            # user.inventory.append(item)
            await self.update_current_room_data(current_room_data)
            return item
        raise ValueError("Item not found in the current room")


    async def item_drop(self, item_id: UUID4, item_name: str):
        user = await self.get_user()
        current_room_data = user.current_room_data

        item = {"id": str(item_id), "name": item_name}
        current_room_data["items"].append(item)
        # Remove item from user's inventory here (pseudo-code)
        # user.inventory.remove(item)
        await self.update_current_room_data(current_room_data)
        return item


    async def traverse_room(self, new_room_id: UUID4):
        user = await self.get_user()
        current_room_data = user.current_room_data

        if str(new_room_id) in current_room_data["connections"]:
            room_generator = RoomGenerator(user.current_world, WorldTier.Tier1)
            new_room_data = room_generator.generate_next_room()
            await self.update_current_room_data(new_room_data)
            return new_room_data
        raise ValueError("New room is not connected to the current room")
