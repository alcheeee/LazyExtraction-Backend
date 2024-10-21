from app.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.user_handler import UserHandler
from app.crud import ItemsCRUD, UserCRUD, UserInventoryCRUD
from app.models import Items

from app.game_systems.items.item_stats_handler import ItemStatsHandler
from app.game_systems.items.items_data import (
    armor_classes,
    weapon_classes,
    bullet_classes,
    medical_classes,
    attachment_classes,
    clothing_classes
)
from app.utils.logger import MyLogger
admin_log = MyLogger.admin()


async def init_content(session):
    items_crud = ItemsCRUD(Items, session)
    item_collections = [
        armor_classes,
        weapon_classes,
        attachment_classes,
        bullet_classes,
        medical_classes,
        clothing_classes
    ]

    for item_class_collection in item_collections:
        for item_class in item_class_collection:
            item_instance = item_class()
            item, detail = item_instance.to_db_models()

            existing_item = await items_crud.check_item_exists(item_instance.item_name)
            if not existing_item:
                session.add(item)
                await session.flush()
                detail.item_id = item.id
                session.add(detail)

    await session.commit()
    return True


class InitializeLazyBot:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_handler = UserHandler(session)
        self.user_crud = UserCRUD(None, session)

        self.username = settings.GAME_BOT_USERNAME
        self.password = settings.GAME_BOT_PASSWORD
        self.email = settings.GAME_BOT_EMAIL
        self.bot_id = None

    async def check_bot_account(self) -> None:
        bot_existing_id = await self.user_crud.get_user_field_from_username(self.username, 'id')
        if bot_existing_id is not None:
            settings.GAME_BOT_USER_ID = bot_existing_id
            self.bot_id = bot_existing_id
        else:
            await self.create_bot_account()

    async def create_bot_account(self) -> None:
        bot_account = await self.user_handler.create_user(
            self.username, self.password, self.email, game_bot=True
        )
        settings.GAME_BOT_USER_ID = int(bot_account.id)
        self.bot_id = int(bot_account.id)

        print('--> Bot Account created')
        await self.make_bot_admin()
        await self.init_bot_inventory()
        print('--> Bot Account Finished Initializing')

    async def make_bot_admin(self) -> None:
        await self.user_crud.make_user_admin(self.bot_id)

    async def init_bot_inventory(self):
        try:
            items_to_give = self.get_items_to_give()

            for item in items_to_give:
                await self.add_item_to_inventory(item)

        except Exception as e:
            MyLogger.log_exception(admin_log, e)

    async def add_item_to_inventory(self, item: str):
        items_crud = ItemsCRUD(Items, self.session)
        user_inv_crud = UserInventoryCRUD(Items, self.session)

        item_db_id = await items_crud.check_item_exists(item)
        new_item = await user_inv_crud.update_user_inventory_item(
            user_id=self.bot_id,
            item_id=item_db_id,
            quantity_change=10,
            to_stash=False
        )
        await self.session.flush()
        return new_item

    @staticmethod
    def get_items_to_give():
        return [
            'M4 Carbine',
            'Holographic (1x)',
            'Holographic (1x-4x)',
            'Compact Foregrip',
            'Precision Long Grip',
            'Heavy Duty Grip',
            'Tactical Short Grip'
        ]
