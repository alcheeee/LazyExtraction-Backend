from typing import Annotated
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Body

from ..auth import UserService, AccessTokenBearer
from ..crud import UserInventoryCRUD, UserCRUD
from ..config import settings
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    DataName,
    MyLogger,
    CommonHTTPErrors,
    exception_decorator
)

from ..models import User, Inventory
from ..schemas import ItemCreate, openapi_item_examples
from ..game_systems.items.item_handler import NewItem


error_log = MyLogger.errors()
admin_log = MyLogger.admin()


game_bot = {
    'username': settings.GAME_BOT_USERNAME,
    'user_id': settings.GAME_BOT_USER_ID
}


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not Found"}}
)


@admin_router.get("/")
async def root(user_data: dict = Depends(AccessTokenBearer())):
    username = user_data['user']['username']
    user_id = int(user_data['user']['user_id'])
    if username != game_bot['username'] and user_id != int(game_bot['user_id']):
        raise CommonHTTPErrors.credentials_error()

    return ResponseBuilder.success("Admin routes ready")


@admin_router.post("/create-item")
@exception_decorator
async def create_item_endpoint(
        request: Annotated[ItemCreate, Body(openapi_examples=openapi_item_examples)],
        admin_username: str = Depends(UserService.check_if_admin),
        session: AsyncSession = Depends(get_db)
):
    new_item = NewItem(session)
    item_data = request.dict()
    response = await new_item.create_item(item_data, admin_request=True)
    await session.commit()

    msg = f"Admin {admin_username} created item {request.item_name}"
    admin_log.info(msg)
    return ResponseBuilder.success(msg, data=response)


class AddItemToUser(BaseModel):
    username: str
    item_id: int
    quantity: int


@admin_router.put("/add-item-to-user")
@exception_decorator
async def add_an_item_to_user(
        request: AddItemToUser,
        session: AsyncSession = Depends(get_db),
        user_data: dict = Depends(AccessTokenBearer()),
):
    username = user_data['user']['username']
    user_id = int(user_data['user']['user_id'])

    if username != game_bot['username'] and user_id != int(game_bot['user_id']):
        raise CommonHTTPErrors.credentials_error()

    user_inventory_crud = UserInventoryCRUD(Inventory, session)
    user_crud = UserCRUD(User, session)

    receiving_inventory_id = await user_crud.get_user_inventory_id_by_username(request.username)
    if not receiving_inventory_id:
        raise CommonHTTPErrors.server_error()

    result = await user_inventory_crud.update_user_inventory_item(
        inventory_id=receiving_inventory_id,
        item_id=request.item_id,
        quantity_change=request.quantity,
        to_stash=True
    )
    await session.commit()
    msg = f"Admin {username} Added/Removed {request.quantity} of item {request.item_id} to {request.username}"
    admin_log.info(msg)
    return ResponseBuilder.success(msg, data=result)






