from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import (joinedload,
                            selectinload)

from fastapi import (APIRouter,
                     HTTPException,
                     Depends)

from ..database.CRUD.BaseCRUD import BaseCRUD
from ..database.db import get_session
from ..models.models import User
from ..models.item_models import Items
from ..auth.auth_handler import get_current_user

from app.game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler
from app.game_systems.gameplay_options import equipment_map

from app.utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()


user_info_router = APIRouter(
    prefix="/user-info",
    tags=["info"],
    responses={404: {"description": "Not Found"}}
)


@user_info_router.get("/get-user-info")
async def get_user_stats(user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            if not user.stats:
                raise HTTPException(status_code=404, detail={"message": "No stats found for the user."})

            stats = user.stats
            user_info = {
                "username": user.username,
                "bank": user.inventory.bank,
                "energy": user.inventory.energy,
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
                "current_job": user.job if user.job else None
            }

            return user_info

        except Exception as e:
            admin_log.error(f"Error getting user stats: {str(e)}")
            raise HTTPException(status_code=500, detail={"message": "Server error"})



@user_info_router.get("/get-user-inventory")
async def get_user_items(user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            if not user.inventory:
                raise HTTPException(status_code=404, detail={"message": "No inventory found for the user."})

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

                    check_for_stats = await ItemStatsHandler(user.id, main_item.id, session).get_item_stats_json(main_item)
                    if check_for_stats:
                        item_info["stats"] = check_for_stats

                item_details.append(item_info)
            return item_details

        except ValueError as e:
            return {"message": f"{str(e)}"}
        except Exception as e:
            admin_log.error(f"Error getting user inventory: {str(e)}")
            raise HTTPException(status_code=500, detail={"message": "Error getting inventory"})


