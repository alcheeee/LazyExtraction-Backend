from pydantic import BaseModel
from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends
from ..models.models import User, Inventory, InventoryItem
from ..models.item_models import Items
from ..auth.auth_handler import get_current_user
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
                item_info = {
                    "item_id": main_item.id,
                    "item_name": main_item.item_name,
                    "item_quality": main_item.quality,
                    "quantity": item.quantity,
                    "category": main_item.category,
                    "item_slot": None
                }
                if main_item.category.value in ['Clothing', 'Weapon']:
                    item_info["category"] = main_item.clothing_details.clothing_type if main_item.category.value == 'Clothing' else 'Weapon'
                    for equipped_id, slot_name in equipped_items_map.items():
                        if item.item_id == equipped_id:
                            item_info["item_slot"] = slot_name
                            break
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
        if isinstance(result, dict) and 'message' in result:
            return result
        else:
            return {"message": f"Item {result} successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})



