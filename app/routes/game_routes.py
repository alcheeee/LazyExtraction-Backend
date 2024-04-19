from pydantic import BaseModel
from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends, status

from .router_ids import RouteIDs
from .routes import user_router
from ..models.models import User, Inventory, InventoryItem
from ..models.item_models import Items
from ..auth.auth_handler import get_current_user
from ..services.job_service import job_service
from app.game_systems.markets.MarketHandlerCRUD import engine
from app.game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler
from app.game_systems.gameplay_options import equipment_map
from app.utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()


game_router = APIRouter(
    prefix="/game",
    tags=["game"],
    responses={404: {"description": "Not Found"}}
)

"""
Routes to add:
1 - User Equipping
    - Inventory checks
2 - Selling items
    - Inventory checks
"""


@game_router.post("/get-user-inventory")
async def get_users_items(user: User = Depends(get_current_user)):
    with Session(engine) as session:
        try:
            session.add(user)
            if not user.inventory:
                raise HTTPException(status_code=404, detail={"message": "No inventory found for the user."})

            equipped_items_map = {
                getattr(user.inventory, slot): category for category, slot in equipment_map.items()
                if getattr(user.inventory, slot) is not None
            }

            item_details = []
            for item in user.inventory.items:
                main_item = session.get(Items, item.item_id)
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
                    
                    check_for_stats = ItemStatsHandler(user.id, main_item.id).get_item_stats_json(session, main_item)
                    if check_for_stats:
                        item_info["stats"] = check_for_stats

                item_details.append(item_info)
            return item_details

        except ValueError as e:
            return {"message": str(e)}
        except Exception as e:
            admin_log.error(f"Error getting user inventory: {str(e)}")
            raise HTTPException(status_code=500, detail={"message": "Error getting inventory"})

class UserItemActionRequest(BaseModel):
    item_id: int

@game_router.post("/equip-item")
async def equip_unequip_inventory_item(request: UserItemActionRequest, user: User = Depends(get_current_user)):
    try:
        result = ItemStatsHandler(user.id, request.item_id).user_equip_unequip_item()
        if result in ["equipped", "unequipped"]:
            return {"message": f"Item {result}"}
        else:
            return HTTPException(status_code=400, detail={"message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})



class UserActionRequest(BaseModel):
    button_id: str

@game_router.post("/user-action")
async def user_action_buttons(request: UserActionRequest, user: User = Depends(get_current_user)):
    route_id = RouteIDs(request.button_id, user)
    result, msg = route_id.find_id()
    if result:
        return {"message": msg}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": msg})



@game_router.post("/get-all-jobs")
async def get_all_job_info(user: User = Depends(get_current_user)):
    with Session(engine) as session:
        try:
            result = job_service.get_all_jobs(session)
            if result:
                return result
            else:
                return HTTPException(status_code=400, detail={"message": "Internal error occured"})
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e)})




