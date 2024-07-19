from fastapi import APIRouter, Depends
from ..auth import current_user
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    DataName,
    MyLogger,
    common_http_errors
)
from ..get_handlers.get_user_info import GetUserInfo
from ..schemas import UserInfoNeeded

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
async def get_user_info(
        request: UserInfoNeeded,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):

    data_name = None
    if request.Inventory:
        data_name = DataName.UserInventory
    elif request.Stats:
        data_name = DataName.UserStats
    elif request.InventoryItems:
        data_name = DataName.InventoryItem

    try:
        get_info = await GetUserInfo(request, user_id, session).get_info()
        return ResponseBuilder.success("", data_name, get_info)

    except Exception as e:
        MyLogger.log_exception(error_log, e, user_id, request)
        raise common_http_errors.server_error()




