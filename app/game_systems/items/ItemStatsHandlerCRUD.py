from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.game_systems.gameplay_options import ItemType, item_bonus_mapper, equipment_map
from app.models.item_models import Items
from app.models.models import User, InventoryItem
from app.utils.logger import MyLogger
game_log = MyLogger.game()
admin_log = MyLogger.admin()
user_log = MyLogger.user()


class ItemStatsHandler:
    def __init__(self, user_id: int, item_id: int, session: AsyncSession):
        self.user_id = user_id
        self.item_id = item_id
        self.session = session


    def check_item_category_map(self, item):
        category_bonus_mapping = {
            "Clothing": item.clothing_details,
            "Weapon": item.weapon_details
        }
        item_stats_source = category_bonus_mapping.get(item.category.value)
        if item_stats_source:
            return item_stats_source


    def get_item_stats_json(self, item):
        item_stats_source = self.check_item_category_map(item)
        if not item_stats_source:
            return None

        item_stats_results = {}
        for stat_key, bonus_attr in item_bonus_mapper.items():
            item_bonus = getattr(item_stats_source, bonus_attr, 0)
            if item_bonus != 0:
                item_stats_results[bonus_attr] = str(item_bonus)

        return item_stats_results


    async def user_equip_unequip_item(self):
        try:
            user = await self.session.get(User, self.user_id)
            item = await self.session.get(Items, self.item_id)

            if not user or not item:
                raise ValueError("User or item not found")
            if item.category not in [ItemType.Clothing, ItemType.Weapon]:
                raise ValueError("Incorrect item type")

            item_slot_type = item.clothing_details.clothing_type if item.category == ItemType.Clothing else "Weapon"
            item_slot_attr = equipment_map.get(item_slot_type)
            current_equipped_item_id = getattr(user.inventory, item_slot_attr)

            target_inventory_item = (await self.session.execute(
                select(InventoryItem).where(
                    InventoryItem.inventory_id == user.inventory.id,
                    InventoryItem.item_id == item.id
                )
            )).scalars().first()

            if not target_inventory_item or target_inventory_item.quantity == 0:
                raise ValueError("You do not have that item")

            equipping_new_item = current_equipped_item_id != item.id

            if equipping_new_item:
                setattr(user.inventory, item_slot_attr, item.id)
                self.adjust_user_stats_item(user, item, equipping=True)

                if current_equipped_item_id:
                    previous_item = await self.session.get(Items, current_equipped_item_id)
                    self.adjust_user_stats_item(user, previous_item, equipping=False)
            else:
                setattr(user.inventory, item_slot_attr, None)
                self.adjust_user_stats_item(user, item, equipping=False)

            action = "equipped" if equipping_new_item else "unequipped"
            user_log.info(f"User {user.username} {action} {item.item_name}")
            return f"{action}"

        except ValueError:
            raise
        except Exception:
            raise


    def adjust_user_stats_item(self, user, item, equipping=True):
        item_stats_source = self.check_item_category_map(item)
        if not item_stats_source:
            raise ValueError(f"No bonus stats available for category: {item.category}")

        try:
            for stat_key, bonus_attr in item_bonus_mapper.items():
                item_bonus = getattr(item_stats_source, bonus_attr, 0)
                if item_bonus:
                    current_value = getattr(user.stats, stat_key, 0)
                    adjustment = item_bonus if equipping else -item_bonus
                    new_value = current_value + adjustment
                    setattr(user.stats, stat_key, new_value)
                    admin_log.debug(f"111 - Adjusted {stat_key}: {current_value} -> {new_value} (Adjustment: {adjustment})")
            user.stats.round_stats()
        except:
            raise





