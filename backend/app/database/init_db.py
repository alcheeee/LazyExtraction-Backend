from ..crud import ItemsCRUD
from ..models import Items
from ..game_systems.items.item_handler import NewItem
from ..game_systems.items.items_data import (
    armor_items,
    weapon_items,
    bullet_items,
    medical_items,
    attachment_items,
    clothing_items
)


async def init_content(session):
    items_crud = ItemsCRUD(Items, session)
    item_collections = [
        armor_items,  # Will Remove
        weapon_items,  # Will Remove
        bullet_items,
        medical_items,
        attachment_items,
        clothing_items
    ]

    for item_collection in item_collections:
        for item_data in item_collection.values():
            existing_item = await items_crud.check_item_exists(item_data['item_name'])
            if not existing_item:
                created_item = await NewItem.initialize_static_items(item_data, session)
                if not created_item:
                    print(f"Failed to create item: {item_data['item_name']}")
    return True


async def create_game_account(session):
    """
    Create the game account for testing purposes, and whatever else may come up (Automod? Random Events?)
    """
    from ..config import settings
    from ..database.user_handler import UserHandler
    from ..crud import UserCRUD, UserInventoryCRUD
    from ..game_systems.items.item_stats_handler import ItemStatsHandler

    user_handler = UserHandler(session)

    username = settings.GAME_BOT_USERNAME
    password = settings.GAME_BOT_PASSWORD
    email = settings.GAME_BOT_EMAIL

    _crud = UserCRUD(None, session)
    bot_existing_id = await _crud.get_user_field_from_username(username, 'id')
    if bot_existing_id:
        settings.GAME_BOT_USER_ID = int(bot_existing_id.id)
        return

    bot_account = await user_handler.create_user(username, password, email, game_bot=True)
    settings.GAME_BOT_USER_ID = int(bot_account.id)

    print('Game bot created')

    try:
        user_crud = UserCRUD(None, session)
        user_inv_crud = UserInventoryCRUD(Items, session)
        items_crud = ItemsCRUD(Items, session)

        await user_crud.make_user_admin(bot_account.id)

        items_to_give = [
            'Tactical Helmet',
            'Tactical Vest',
            'M4A1 Carbine',
            'Recon Bandana',
            'Tactical Hoodie',
            'Cargo Pants'
        ]
        for item in items_to_give:
            item_db_id = await items_crud.check_item_exists(item)
            new_inventory_item = await user_inv_crud.update_user_inventory_item(
                inventory_id=bot_account.inventory_id,
                item_id=item_db_id,
                quantity_change=1,
                to_stash=False
            )
            await user_inv_crud.update_user_inventory_item(
                inventory_id=bot_account.inventory_id,
                item_id=item_db_id,
                quantity_change=1,
                inventory_item=new_inventory_item,
                to_stash=True
            )

            item_stats_handler = ItemStatsHandler(bot_account.id, item_db_id, session)
            await item_stats_handler.user_equip_unequip_item()

    except Exception as e:
        print(str(e))



