from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import BaseModel
from ..models.models import User
from ..auth.auth_handler import get_current_user
from app.models.item_models import GeneralMarket, Items
from app.game_systems.markets.MarketHandlerCRUD import MarketTransaction, engine
from app.database.UserCRUD import user_crud
from app.utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()

market_router = APIRouter(
    prefix="/game/market",
    tags=["market"],
    responses={404: {"description": "Not Found"}}
)


@market_router.post("/get-generalmarket-items")
async def get_all_generalmarket_items(user: User = Depends(get_current_user)):
    with Session(engine) as session:
        try:
            items = session.exec(select(GeneralMarket)).all()
            result = []
            for item in items:
                item_data = {
                    "item_id": item.item_id,
                    "item_name": item.item.item_name,
                    "item_quality": item.item_quality,
                    "quantity": item.item_quantity,
                    "item_cost": item.item_cost,
                    "sell_price": item.sell_price
                }
                result.append(item_data)
            return result

        except Exception as e:
            admin_log.error(str(e))
            return {"message": "Error getting inventory"}

class MarketPurchaseRequest(BaseModel):
    item_id: int
    quantity: int

@market_router.post("/buy-market-item")
async def buy_market_items(request: MarketPurchaseRequest, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        transaction = session.begin()
        try:
            session.add(user)
            item = session.get(Items, request.item_id)
            if not item:
                admin_log.error(f"{user.username} - item not found.")
                raise HTTPException(status_code=404, detail="Item not found")

            if request.quantity <= 0:
                game_log.error(f"{user.username} tried to purchase {request.quantity} of {item.id}.")
                raise HTTPException(status_code=400, detail="Invalid quantity")

            total_cost = item.general_market_items.item_cost * request.quantity
            if user.inventory.bank < total_cost:
                user_log.info(f"{user.username} doesn't have enough for {item.item_name}.")
                raise HTTPException(status_code=403, detail="Insufficient funds")

            if item.general_market_items.item_quantity < request.quantity:
                user_log.error(f"{user.username} - Tried to buy more than available stock.")
                raise HTTPException(status_code=400, detail="Not enough stock available")

            user.inventory.bank -= total_cost
            item.general_market_items.item_quantity -= request.quantity
            session.commit()
            user_crud.update_user_inventory(user.id, item.id, request.quantity)
            user_log.info(f"{user.username} purchased {request.quantity} of {item.item_name}.")
            return {"message": f"Purchased {request.quantity} of {item.item_name}"}

        except Exception as e:
            session.rollback()
            admin_log.error(f"{user.username} - Error purchasing item due to: {e}")
            return {"message": "Error purchasing item"}



