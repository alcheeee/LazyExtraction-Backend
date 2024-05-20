from fastapi import APIRouter, Depends

from ..game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler
from ..schemas.item_schema import equipment_map

from ..auth.auth_handler import get_current_user
from ..models import (
    User,
    Items
)


from . import (
    AsyncSession,
    dependency_session,
    ResponseBuilder,
    common_http_errors,
)


user_info_router = APIRouter(
    prefix="/user-info",
    tags=["info"],
    responses={404: {"description": "Not Found"}}
)


@user_info_router.get("/get-user-info")
async def get_user_stats(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        if not user.stats:
            raise common_http_errors.server_error()

        stats = user.stats
        inventory = user.inventory
        user_info = {
            "username": user.username,
            "bank": inventory.bank,
            "energy": inventory.energy,
            "level": stats.level,
            "reputation": stats.reputation,
            "max_energy": stats.max_energy,
            "evasiveness": stats.evasiveness,
            "health": stats.health,
            "strength": stats.strength,
            "knowledge": stats.knowledge,
            "luck": stats.luck,
            "damage": stats.damage,
            "education": stats.education,
            "current_job": stats.job if stats.job else None
        }

        return user_info

    except Exception as e:
        error_log.error(f"Error getting user stats: {str(e)}")
        raise common_http_errors.server_error()



@user_info_router.get("/get-user-inventory")
async def get_user_items(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        session.add(user)
        if not user.inventory:
            raise Exception("No inventory found for the user.")

        equipped_items_map = {
            getattr(user.inventory, slot): category for category, slot in equipment_map.items()
            if getattr(user.inventory, slot) is not None
        }

        item_details = []
        for item in user.inventory.items:
            if item.quantity <= 0:
                continue
            main_item = await session.get(Items, item.item_id)
            if main_item.general_market_items:
                item_cost = main_item.general_market_items.item_cost
                sell_price = main_item.general_market_items.sell_price
            else:
                item_cost = None
                sell_price = None
            item_info = {
                "item_id": main_item.id,
                "item_name": main_item.item_name,
                "item_quality": main_item.quality,
                "quantity": item.quantity,
                "illegal": main_item.illegal,
                "category": main_item.category.value,
                "slot_type": None,
                "equipped_slot": None,
                "item_cost": item_cost,
                "sell_price": sell_price
            }

            if main_item.category.value in ['Clothing', 'Weapon']:
                item_info["slot_type"] = (main_item.clothing_details.clothing_type if
                                          main_item.category.value == 'Clothing' else 'Weapon')

                for equipped_id, slot_name in equipped_items_map.items():
                    if item.item_id == equipped_id:
                        item_info["equipped_slot"] = slot_name
                        break

                item_handler = ItemStatsHandler(user, main_item.id, session)
                check_for_stats = item_handler.get_item_stats_json(main_item)
                if check_for_stats:
                    item_info["stats"] = check_for_stats

            item_details.append(item_info)
        return item_details

    except ValueError as e:
        return ResponseBuilder.error(str(e))
    except Exception as e:
        error_log.error(f"Error getting user inventory: {str(e)}")
        raise common_http_errors.server_error()


