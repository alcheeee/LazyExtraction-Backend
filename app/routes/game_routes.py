from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import BaseModel
from ..models.models import User
from ..auth.auth_handler import get_current_user
from app.models.item_models import GeneralMarket, Items
from app.game_systems.markets.market_handler import MarketTransaction, engine
from app.database.UserCRUD import user_crud
from app.utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()


game_router = APIRouter(
    prefix="/game/",
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



@game_router.post("/get-generalmarket-items")
async def get_all_generalmarket_items(user: User = Depends(get_current_user)):
    pass