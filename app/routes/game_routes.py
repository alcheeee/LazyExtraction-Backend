from pydantic import BaseModel
from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends
from ..models.models import User, Inventory, InventoryItem
from ..auth.auth_handler import get_current_user
from app.game_systems.markets.MarketHandlerCRUD import engine
from app.game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler
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
                raise HTTPException(status_code=404, detail="No inventory found for the user.")

            inventory_items = user.inventory.items
            item_details = [{
                "item_id": item.item_id,
                "item_name": item.item.item_name,
                "item_quality": item.item.quality,
                "quantity": item.quantity,
                "category": item.item.category
            } for item in inventory_items]
            return item_details

        except ValueError as e:
            return {"message": str(e)}
        except Exception as e:
            admin_log.error(f"Error getting user inventory: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting inventory")

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
        raise HTTPException(status_code=400, detail=str(e))



