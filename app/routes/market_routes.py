from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import BaseModel
from ..models.models import User
from ..auth.auth_handler import get_current_user
from app.models.item_models import GeneralMarket, Items
from app.game_systems.markets.market_handler import MarketTransaction, engine
from app.utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()

market_router = APIRouter(
    prefix="/user/market",
    tags=["market"],
    responses={404: {"description": "Not Found"}}
)


@market_router.post("/get-generalmarket-items")
async def get_all_generalmarket_items(user: User = Depends(get_current_user)):
    with Session(engine) as session:
        items = session.exec(select(GeneralMarket)).all()
        result = []
        for item in items:
            item_data = {
                "item_id": item.item.hash,
                "item_name": item.item.item_name,
                "item_cost": item.item_cost,
                "sell_price": item.sell_price,
                "quantity": item.item_quantity
            }
            result.append(item_data)
        return result


class MarketPurchaseRequest(BaseModel):
    item_hash: str
    quantity: int

@market_router.post("/buy-market-item")
async def buy_market_items(request: MarketPurchaseRequest, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        transaction = session.begin()
        try:
            item = session.exec(select(Items).where(Items.hash == request.item_hash)).first()
            if not item:
                admin_log.error(f"{user.username} item not found.")
                raise HTTPException(status_code=404, detail="Item not found")

            if user.inventory.bank < item.general_market_items.item_cost * request.quantity:
                user_log.info(f"{user.username} doesn't have enough for {item.item_name}.")
                raise HTTPException(status_code=403, detail="Insufficient funds")

            user.inventory.bank -= item.general_market_items.item_cost * request.quantity
            item.general_market_items.item_quantity -= request.quantity
            if item.general_market_items.item_quantity < 0:
                session.rollback()
                user_log.error(f"{user.username} - Tried to buy more than available stock of {item.general_market_items.item_quantity}")
                raise HTTPException(status_code=400, detail="Not enough stock available")

            session.commit()
            user_log.info(f"{user.username} purchased {request.quantity} of {item.item_name}.")
            return {"message": f"Purchased {item.item_name}"}

        except Exception as e:
            session.rollback()
            admin_log.error(f"{user.username} - Error purchasing item due to: {e}")
            return {"message": f"Error purchasing item."}


