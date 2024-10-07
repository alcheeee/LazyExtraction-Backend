from typing import Annotated
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Body

from app.auth import UserService, AccessTokenBearer
from app.crud import UserInventoryCRUD, UserCRUD, UserBankingCRUD
from app.settings import settings

from . import (
    DataName,
    AsyncSession,
    ResponseBuilder,
    error_responses,
    MyLogger,
    CommonHTTPErrors,
    exception_decorator
)
from app.dependencies.get_db import get_db
from app.models import User, Inventory


error_log = MyLogger.errors()
admin_log = MyLogger.admin()


game_bot = {
    'username': settings.GAME_BOT_USERNAME,
    'user_id': settings.GAME_BOT_USER_ID
}


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses=error_responses
)


@admin_router.get("/")
async def root(user_data: dict = Depends(AccessTokenBearer())):
    username = user_data['user']['username']
    user_id = int(user_data['user']['user_id'])
    if username != game_bot['username'] and user_id != int(game_bot['user_id']):
        raise CommonHTTPErrors.credentials_error()
    return ResponseBuilder.success("Admin routes ready")


@admin_router.post("/adjust-money")
@exception_decorator
async def adjust_admin_money(
        request: int,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    username = user_data['user']['username']
    user_id = int(user_data['user']['user_id'])
    if username != game_bot['username'] and user_id != int(game_bot['user_id']):
        raise CommonHTTPErrors.credentials_error()
    
    banking_crud = UserBankingCRUD(session=session)
    new_bank_amount = await banking_crud.update_bank_balance_by_username('admin', request)
    await session.commit()
    return ResponseBuilder.success(
        f"Added ${request} to admin", data_name=DataName.UserData, data={'bank': new_bank_amount}
    )


@admin_router.post("/adjust-in-raid")
@exception_decorator
async def adjust_admin_in_raid(
        request: bool,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    username = user_data['user']['username']
    user_id = int(user_data['user']['user_id'])
    if username != game_bot['username'] and user_id != int(game_bot['user_id']):
        raise CommonHTTPErrors.credentials_error()

    admin = await session.get(User, int(user_data['user']['user_id']))
    if not admin:
        return

    admin.in_raid = request
    await session.commit()
    return ResponseBuilder.success(
        message="Admin raid status changed", data_name=DataName.UserData, data={'in_raid': admin.in_raid}
    )


@admin_router.put("/fill-database")
@exception_decorator
async def fill_database_with_test_data(
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    username = user_data['user']['username']
    user_id = int(user_data['user']['user_id'])
    if username != game_bot['username'] and user_id != int(game_bot['user_id']):
        raise CommonHTTPErrors.credentials_error()

    if not settings.TESTING:
        raise ValueError("Not in Testing")

    from app.tests.data_generators.data_handler import CreateTestData
    await CreateTestData(session).create_mock_data()
    return ResponseBuilder.success(message="Database filled with test data")



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

    receiving_user_id = await user_crud.get_user_field_from_username(request.username, 'id')
    if not receiving_user_id:
        raise CommonHTTPErrors.server_error()

    result = await user_inventory_crud.update_user_inventory_item(
        user_id=receiving_user_id,
        item_id=request.item_id,
        quantity_change=request.quantity,
        to_stash=True
    )
    await session.commit()
    msg = f"Admin {user_data['user']['username']} Added/Removed {request.quantity} of item {request.item_id} to {request.username}"
    admin_log.info(msg)
    return ResponseBuilder.success(msg, data=result)






