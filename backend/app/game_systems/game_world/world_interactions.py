from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from ...crud import UserCRUD, UserInventoryCRUD, ItemsCRUD
from ...schemas import RoomInteraction, InteractionTypes
from .world_handler import RoomGenerator
from ...utils import RetryDecorators


class InteractionHandler:
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id
        self.user_crud = UserCRUD(None, session)
        self.item_crud = ItemsCRUD(None, session)
        self.user_inv_crud = UserInventoryCRUD(None, session)

    @RetryDecorators.function_retry_decorator(retry_exceptions=(IntegrityError,))
    async def handle(self, interaction: RoomInteraction):
        user = await self.user_crud.get_user_for_interaction(self.user_id)

        if interaction.action == InteractionTypes.Pickup:
            result = await self.item_pickup(user, interaction.id)
        elif interaction.action == InteractionTypes.Traverse:
            result = await self.traverse_room(user, interaction.id)
        elif interaction.action == InteractionTypes.Extract:
            result = await self.extract_from_raid(user)
        else:
            raise ValueError("Invalid action")

        await self.user_crud.update_user_after_interaction(user)
        return result

    async def item_pickup(self, user, item_id: int):
        room_data = user.current_room_data
        item = next((item for item in room_data["items"] if item["id"] == item_id), None)
        if not item:
            raise ValueError("Item not in room")

        item_db = await self.item_crud.check_item_exists(item['name'])
        if not item_db:
            raise ValueError("Couldn't find a reference to that item")

        room_data["items"].remove(item)
        user.current_room_data = room_data
        flag_modified(user, "current_room_data")

        await self.user_inv_crud.update_user_inventory_item(
            user.inventory_id,
            item_db.id,
            1,
            in_stash=False
        )

        user.stats.knowledge += 0.05
        user.stats.round_stats()
        user.actions_left -= 1

        item['skill-adjustments'] = {
            "knowledge-adjustment": 0.05
        }
        return item

    @staticmethod
    async def traverse_room(user, new_room_id: int):
        current_room_data = user.current_room_data

        if new_room_id in current_room_data["connections"]:
            room_generator = RoomGenerator(user.current_world)
            new_room_data = await room_generator.generate_room()

            user.stats.knowledge += 0.1
            user.stats.level += 0.1
            user.stats.round_stats()

            user.current_room_data = new_room_data
            user.actions_left -= 1

            new_room_data["skill-adjustments"] = {
                "knowledge-adjustment": 0.1,
                "level-adjustment": 0.1
            }
            return new_room_data
        raise ValueError("New room is not connected to the current room")

    @staticmethod
    async def extract_from_raid(user):
        if user.actions_left > 0:
            raise ValueError(f"You still need to perform {user.actions_left} actions")

        user.in_raid = False
        user.actions_left = None
        user.current_world = None
        user.current_room_data = None

        user.stats.level += 0.75
        user.stats.round_stats()

        skill_adjustments = {
            "level-adjustment": 0.75
        }

        return skill_adjustments
