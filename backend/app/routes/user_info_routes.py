from fastapi import APIRouter, Depends
from ..auth import current_user
from ..models import (
    User,
    Items
)
from . import (
    AsyncSession,
    dependency_session,
    ResponseBuilder,
    DataName,
    MyLogger,
    common_http_errors
)


user_info_router = APIRouter(
    prefix="/user-info",
    tags=["info"],
    responses={404: {"description": "Not Found"}}
)


@user_info_router.get("/get-user-info")
async def get_user_stats(
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        pass

    except Exception as e:
        raise common_http_errors.server_error()



@user_info_router.get("/get-user-inventory")
async def get_user_items(
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        pass

    except ValueError as e:
        return ResponseBuilder.error(str(e))
    except Exception as e:
        raise common_http_errors.server_error()


