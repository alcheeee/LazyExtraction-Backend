from fastapi import APIRouter, Depends
from ..auth import current_user
from . import (
    AsyncSession,
    dependency_session,
    ResponseBuilder,
    DataName,
    MyLogger,
    common_http_errors
)
from ..get_handlers.get_user_info import GetUserInfo
from ..schemas import UserInfoNeeded


user_info_router = APIRouter(
    prefix="/user-info",
    tags=["info"],
    responses={404: {"description": "Not Found"}}
)


@user_info_router.get("/get-user-info")
async def get_user_info(
        option: UserInfoNeeded,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
):

    data_name = None
    if option.Inventory:
        data_name = DataName.UserInventory
    elif option.Stats:
        data_name = DataName.UserStats
    elif option.InventoryItems:
        data_name = DataName.InventoryItem

    try:
        get_info = await GetUserInfo(option, user_id, session).get_info()
        return ResponseBuilder.success("", data_name, get_info)

    except Exception as e:
        raise common_http_errors.server_error()




