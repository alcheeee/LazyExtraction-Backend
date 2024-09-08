from typing import Annotated
from fastapi import APIRouter, Depends, Body
from ..auth import current_user
from ..crud import UserInventoryCRUD, UserCRUD
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    DataName,
    MyLogger,
    common_http_errors,
    exception_decorator
)
from ..models import User, Inventory
from ..schemas import ItemCreate, openapi_item_examples
from ..game_systems.items.item_handler import NewItem


error_log = MyLogger.errors()
admin_log = MyLogger.admin()


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not Found"}}
)


@admin_router.get("/")
async def root(admin_username: str = Depends(current_user.check_if_admin)):
    return ResponseBuilder.success("Admin routes ready")


@admin_router.post("/create-item")
@exception_decorator
async def create_item_endpoint(
        request: Annotated[ItemCreate, Body(openapi_examples=openapi_item_examples)],
        admin_username: str = Depends(current_user.check_if_admin),
        session: AsyncSession = Depends(get_db)
):
    new_item = NewItem(session)
    item_data = request.dict()
    response = await new_item.create_item(item_data, admin_request=True)
    await session.commit()

    msg = f"Admin {admin_username} created item {request.item_name}"
    admin_log.info(msg)
    return ResponseBuilder.success(msg, DataName.ItemDetails, response)


@admin_router.put("/add-item-to-user/{username}/{item_id}/{quantity}")
@exception_decorator
async def add_an_item_to_user(
        username: str, item_id: int, quantity: int,
        session: AsyncSession = Depends(get_db),
        admin_username: str = Depends(current_user.check_if_admin)
):

    user_inventory_crud = UserInventoryCRUD(Inventory, session)
    user_crud = UserCRUD(User, session)

    receiving_inventory_id = await user_crud.get_user_inventory_id_by_username(username)
    if not receiving_inventory_id:
        raise common_http_errors.server_error()

    result = await user_inventory_crud.update_user_inventory_item(
        inventory_id=receiving_inventory_id,
        item_id=item_id,
        quantity_change=quantity
    )
    await session.commit()
    msg = f"Admin {admin_username} Added/Removed {quantity} of item {item_id} to {username}"
    admin_log.info(msg)
    return ResponseBuilder.success(msg, DataName.ItemGiven, result)






