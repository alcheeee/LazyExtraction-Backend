from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import BaseModel
from ..models.models import User, InventoryItem
from ..auth.auth_handler import get_current_user
from app.models.item_models import GeneralMarket, Items
from app.game_systems.markets.MarketHandlerCRUD import engine
from app.database.UserCRUD import user_crud
from app.utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()

market_router = APIRouter(
    prefix="/market",
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
                    "sell_price": item.sell_price,
                    "category": item.item.category.value
                }
                result.append(item_data)
            return result

        except Exception as e:
            admin_log.error(str(e))
            return {"message": "Error getting inventory"}

class MarketTransactionRequest(BaseModel):
    item_id: int
    quantity: int

@market_router.post("/buy-market-item")
async def buy_market_items(request: MarketTransactionRequest, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        transaction = session.begin()
        try:
            session.add(user)
            item = session.get(Items, request.item_id)
            if not item:
                raise HTTPException(status_code=404, detail={"message": "Item not found"})

            if request.quantity <= 0:
                raise HTTPException(status_code=400, detail={"message": "Invalid quantity"})

            if not hasattr(item, 'general_market_items') or item.general_market_items is None:
                raise HTTPException(status_code=404, detail={"message": "Market item not found"})

            total_cost = item.general_market_items.item_cost * request.quantity
            if user.inventory.bank < total_cost:
                raise HTTPException(status_code=403, detail={"message": "Insufficient funds"})

            if item.general_market_items.item_quantity < request.quantity:
                raise HTTPException(status_code=400, detail={"message": "Not enough stock available"})

            user.inventory.bank -= total_cost
            item.general_market_items.item_quantity -= request.quantity
            result = user_crud.update_user_inventory(user.id, item.id, request.quantity, selling=False, session=session)
            if not result:
                raise HTTPException(status_code=400, detail={"message": "Failed to update inventory properly."})

            session.commit()
            user_log.info(f"{user.username} purchased {request.quantity} of {item.item_name}.")
            return {"message": f"Bought {request.quantity} of {item.item_name}, for {total_cost}."}

        except HTTPException as he:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            admin_log.error(f"{user.username} - Error purchasing item due to: {e}")
            return {"message": "Error purchasing item"}


@market_router.post("/sell-market-item")
async def sell_market_items(request: MarketTransactionRequest, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        transaction = session.begin()
        try:
            session.add(user)
            item = session.get(Items, request.item_id)
            if not item:
                raise HTTPException(status_code=404, detail={"message": "Item not found"})

            if request.quantity <= 0:
                raise HTTPException(status_code=400, detail={"message": "Invalid quantity"})

            if not hasattr(item, 'general_market_items') or item.general_market_items is None:
                raise HTTPException(status_code=404, detail={"message": "Market item not found"})

            total_earning = item.general_market_items.sell_price * request.quantity

            inventory_item = session.query(InventoryItem).filter_by(
                inventory_id=user.inventory.id, item_id=item.id).first()

            if inventory_item is None or inventory_item.quantity < request.quantity:
                raise HTTPException(status_code=400, detail={"message": "Not enough items to sell"})

            user.inventory.bank += total_earning
            item.general_market_items.item_quantity += request.quantity
            result = user_crud.update_user_inventory(user.id, item.id, request.quantity, selling=True, session=session)
            if not result:
                raise HTTPException(status_code=400, detail={"message": "Failed to update inventory properly."})

            session.commit()
            user_log.info(f"{user.username} sold {request.quantity} of {item.item_name}.")
            return {"message": f"Sold {request.quantity} of {item.item_name}, earning {total_earning}."}

        except HTTPException as he:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            admin_log.error(f"{user.username} - Error selling item due to: {e}")
            return {"message": str(e)}

