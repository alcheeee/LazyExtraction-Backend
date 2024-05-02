from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from ...crud.BaseCRUD import BaseCRUD
from ...schemas.item_schema import ItemType, equipment_map, item_bonus_mapper
from ...models.item_models import Items, Clothing
from ...models.models import User, InventoryItem
from ...utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()
user_log = MyLogger.user()


class ItemStatsHandler:
    def __init__(self, user_id, item_id: int, session: AsyncSession):
        self.user_id = user_id
        self.item_id = item_id
        self.session = session
        self.user_crud = BaseCRUD(User, session)
        self.item_crud = BaseCRUD(Items, session)
        self.inventory_item_crud = BaseCRUD(InventoryItem, session)

    def get_item_category(self, item):
        if item.category == ItemType.Clothing:
            return item.clothing_details
        elif item.category == ItemType.Weapon:
            return item.weapon_details
        return None


    def get_item_stats_json(self, item):
        item_stats_source = self.get_item_category(item)
        if not item_stats_source:
            return None

        item_stats_results = {}
        for stat_key, bonus_attr in item_bonus_mapper.items():
            item_bonus = getattr(item_stats_source, bonus_attr, 0)
            if item_bonus != 0 and item_bonus:
                item_stats_results[bonus_attr] = item_bonus
        return item_stats_results


    async def user_equip_unequip_item(self):
        try:
            user = await self.user_crud.get_by_id(self.user_id, options=[
                selectinload(User.inventory),
                selectinload(User.stats)
            ])
            if not user:
                raise Exception("User not found")

            item = await self.item_crud.get_by_id(self.item_id, options=[
                joinedload(Items.clothing_details),
                joinedload(Items.weapon_details)
            ])
            if not item:
                raise ValueError("Incorrect item type")

            item_details = self.get_item_category(item)
            if not item_details:
                raise ValueError(f"No details available for category: {item.category}")

            item_slot_type = item_details.clothing_type if isinstance(item_details, Clothing) else "Weapon"
            item_slot_attr = equipment_map.get(item_slot_type)

            current_equipped_item_id = getattr(user.inventory, item_slot_attr)

            target_inventory_item = await self.inventory_item_crud.get_inventory_item_by_conditions(
                user.inventory.id, item.id
            )

            if not target_inventory_item or target_inventory_item.quantity == 0:
                raise ValueError("You do not have that item")

            equipping_new_item = current_equipped_item_id != item.id
            if equipping_new_item:
                setattr(user.inventory, item_slot_attr, item.id)
                self.adjust_user_stats_item(user, item_details, equipping=True)

                if current_equipped_item_id:
                    previous_item_details = self.get_item_category(await self.item_crud.get_by_id(current_equipped_item_id))
                    self.adjust_user_stats_item(user, previous_item_details, equipping=False)
            else:
                setattr(user.inventory, item_slot_attr, None)
                self.adjust_user_stats_item(user, item_details, equipping=False)

            action = "equipped" if equipping_new_item else "unequipped"
            return action

        except ValueError:
            raise
        except Exception:
            raise


    def adjust_user_stats_item(self, user, item_details, equipping=True):
        if not item_details:
            raise ValueError("No item details provided for stat adjustment")
        try:
            for stat_key, bonus_attr in item_bonus_mapper.items():
                item_bonus = getattr(item_details, bonus_attr, 0)
                if item_bonus:
                    current_value = getattr(user.stats, stat_key, 0)
                    adjustment = item_bonus if equipping else -item_bonus
                    new_value = current_value + adjustment
                    setattr(user.stats, stat_key, new_value)
            user.stats.round_stats()
        except Exception as e:
            raise





