from fastapi import APIRouter, Depends
from app.auth import AccessTokenBearer
from . import (
    DataName,
    AsyncSession,
    ResponseBuilder,
    MyLogger,
    CommonHTTPErrors,
    exception_decorator
)
from app.dependencies.get_db import get_db
from app.get_handlers.get_user_info import GetUserInfo
from app.schemas import UserInfoNeeded
from app.models import InventoryItem, Inventory, Stats

error_log = MyLogger.errors()

info_router = APIRouter(
    prefix="/info",
    tags=["info"],
    responses={404: {"description": "Not Found"}}
)


@info_router.get("/")
async def root():
    return ResponseBuilder.success("Info routes ready")


@info_router.get("/get-user-info")
@exception_decorator
async def get_user_info(
        request: UserInfoNeeded,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    user_id = int(user_data['user']['user_id'])
    data_name = None
    match request:
        case UserInfoNeeded.Inventory:
            data_name = DataName.UserInventory
        case UserInfoNeeded.Stats:
            data_name = DataName.UserStats
        case UserInfoNeeded.InventoryItems:
            data_name = DataName.AllInventoryItems

    get_info = await GetUserInfo(request, user_id, session).get_info()
    return ResponseBuilder.success("", data_name, get_info)





