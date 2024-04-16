from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends
from ..models.models import User, Inventory, InventoryItem
from ..auth.auth_handler import get_current_user
from app.game_systems.markets.MarketHandlerCRUD import engine
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
async def get_all_generalmarket_items(user: User = Depends(get_current_user)):
    with Session(engine) as session:
        try:
            session.add(user)
            if not user.inventory:
                raise HTTPException(status_code=404, detail="No inventory found for the user.")

            inventory_items = user.inventory.items
            item_details = [{
                "item_id": item.item_id,
                "item_name": item.item.item_name,
                "quantity": item.quantity,
                "equipped": item.equipped
            } for item in inventory_items]
            return item_details

        except Exception as e:
            admin_log.error(f"Error getting user inventory: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting inventory")