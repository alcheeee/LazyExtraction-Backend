from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
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
        elif interaction.action == InteractionTypes.Extract:
            extraction = await self.extract_from_raid()
            return extraction
        else:
            raise ValueError("Invalid action")


    async def get_user(self):
        return await self.user_crud.get_user(self.user_id)


    async def item_pickup(self, item_id: UUID4):
        user = await self.get_user()
        room_data = user.current_room_data

        item = next((item for item in room_data["items"] if item["id"] == str(item_id)), None)
        if not item:
            raise ValueError("Item not in room")

        item_db = await self.item_crud.check_item_exists(item['name'])
        if not item_db:
            raise ValueError("Couldn't find a reference to that item")

        room_data["items"].remove(item)
        user.current_room_data = room_data
        flag_modified(user, "current_room_data")

        user_stats = await self.user_crud.get_user_stats(user)
        user_stats.knowledge += 0.05
        user_stats.round_stats()

        await self.user_inv_crud.update_user_inventory_item(
            user.inventory_id,
            item_db.id,
            1,
            in_stash=False
        )
        user.actions_left -= 1

        item['skill-adjustments'] = {
            "knowledge-adjustment": 0.05
        }

        return item


    async def traverse_room(self, new_room_id: UUID4):
        user = await self.get_user()
        current_room_data = user.current_room_data

        if str(new_room_id) in current_room_data["connections"]:
            room_generator = RoomGenerator(user.current_world, WorldTier.Tier1)
            new_room_data = room_generator.generate_next_room()

            user_stats = await self.user_crud.get_user_stats(user)
            user_stats.knowledge += 0.1
            user_stats.level += 0.1
            user_stats.round_stats()

            user.current_room_data = new_room_data
            user.actions_left -= 1

            new_room_data["skill-adjustments"] = {
                "knowledge-adjustment": 0.1,
                "level-adjustment": 0.1
            }
            return new_room_data

        raise ValueError("New room is not connected to the current room")


    async def extract_from_raid(self):
        user = await self.get_user()
        if user.actions_left > 0:
            raise ValueError(f"You still need to perform {user.actions_left} actions")

        user.in_raid = False
        user.actions_left = None
        user.current_world = None
        user.current_room_data = None

        user_stats = await self.user_crud.get_user_stats(user)
        user_stats.level += 0.75
        user_stats.round_stats()

        skill_adjustments = {
            "level-adjustment": 0.75
        }

        return skill_adjustments


















