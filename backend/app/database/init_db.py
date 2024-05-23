from ..crud import ItemsCRUD
from ..models import Items
from ..game_systems.items.ItemHandler import NewItem
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
        for item_variants in item_collection.values():
            for item_data in item_variants.values():
                existing_item = await items_crud.check_item_exists(item_data['item_name'])
                if not existing_item:
                    created_item = await NewItem.initialize_static_items(item_data, session)
                    if created_item:
                        print(f"Created item: {item_data['item_name']}")
                    else:
                        print(f"Failed to create item: {item_data['item_name']}")

    return True

