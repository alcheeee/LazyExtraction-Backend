from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from ..game_systems.items.ItemHandler import ItemCreator
from ..game_systems.markets.MarketHandlerCRUD import BackendMarketHandler
from ..models.models import User
from ..auth.auth_handler import current_user
from ..schemas.item_schema import MarketItemAdd, ItemStats
from ..database.UserHandler import UserHandler
from ..services.RaiseHTTPErrors import raise_http_error
from ..database.db import get_session
from ..utils.logger import MyLogger
admin_log = MyLogger.admin()


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not Found"}}
)


@admin_router.post("/create-item/equippable")
async def create_equippable_item_endpoint(request: ItemStats,
                                          admin_username: str = Depends(current_user.check_if_admin)):
    async with get_session() as session:
        try:
            item_creator = ItemCreator(item_details=request, session=session)
            response_json = await item_creator.create_item()
            return {"message": f"Admin {admin_username} created an item successfully", "item_details": response_json}

        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise raise_http_error.server_error()


@admin_router.post("/add-item-to-market")
async def add_item_to_market(request: MarketItemAdd,
                             admin_username: str = Depends(current_user.check_if_admin)):
    async with get_session() as session:
        try:
            market_handler = BackendMarketHandler(request.item_id, request.market_name,
                                                  request.item_cost, request.sell_price, session)
            result = await market_handler.add_item_to_market()
            if not result:
                raise raise_http_error.mechanics_error("Failed to add item to market")
            return {"message": f"Added {request.item_id} to {request.market_name}"}

        except ValueError as e:
            await session.rollback()
            raise raise_http_error.mechanics_error(str(e))
        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise raise_http_error.server_error()


@admin_router.post("/add-item-to-user/{username}/{item_id}/{quantity}")
async def add_an_item_to_user(username: str, item_id: int,quantity: int,
                              admin_username: str = Depends(current_user.check_if_admin)):

    async with get_session() as session:
        receiving_user = (await session.execute(
            select(User).where(
                User.username == username)
        )).scalars().first()

        if not receiving_user:
            raise HTTPException(status_code=400, detail={"message": f"Couldn't find user."})
        try:
            session.add(receiving_user)
            user_handler = UserHandler(session)
            await user_handler.update_user_inventory(receiving_user.id, item_id,
                                                  quantity, selling=False)
            await session.commit()
            return {"message": f"Added {quantity} of item {item_id} to {receiving_user.username}"}

        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=500, detail={"message": f"Internal Error"})





