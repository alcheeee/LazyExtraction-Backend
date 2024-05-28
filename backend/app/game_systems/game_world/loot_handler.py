from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from ...crud import UserCRUD, WorldCRUD, UserInventoryCRUD, ItemsCRUD
from ...schemas import RoomInteraction, WorldTier, InteractionTypes
from .world_handler import RoomGenerator


class InteractionHandler:
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id
        self.user_crud = UserCRUD(None, session)
        self.item_crud = ItemsCRUD(None, session)
        self.user_inv_crud = UserInventoryCRUD(None, session)


    async def handle(self, interaction: RoomInteraction):
        if interaction.action == InteractionTypes.Pickup:
            item = await self.item_pickup(interaction.id)
            return item
        elif interaction.action == InteractionTypes.Traverse:
            new_room_data = await self.traverse_room(interaction.id)
            return new_room_data
        else:
            raise ValueError("Invalid action")


    async def get_user(self):
        return await self.user_crud.get_user(self.user_id)


    async def item_pickup(self, item_id: UUID4):
        user = await self.get_user()
        current_room_data = user.current_room_data

        item = next((item for item in current_room_data["items"] if item["id"] == str(item_id)), None)
        item_db = await self.item_crud.check_item_exists(item['name'])

        if item and item_db:
            current_room_data["items"].remove(item)
            await self.user_inv_crud.update_user_inventory_item(
                user.inventory_id,
                item_db.id,
                1,
                in_stash=False
            )
            user.current_room_data = current_room_data
            return item
        raise ValueError("Item not found in the current room")


    async def traverse_room(self, new_room_id: UUID4):
        user = await self.get_user()
        current_room_data = user.current_room_data

        if str(new_room_id) in current_room_data["connections"]:
            room_generator = RoomGenerator(user.current_world, WorldTier.Tier1)
            new_room_data = room_generator.generate_next_room()

            user.current_room_data = new_room_data
            return new_room_data
        raise ValueError("New room is not connected to the current room")




















