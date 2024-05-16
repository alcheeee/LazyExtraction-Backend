from fastapi import APIRouter, HTTPException, Depends
from ..models.models import User
from ..models.corp_models import Corporation
from ..schemas.corporation_schema import NewCorporationInfo
from ..auth.auth_handler import current_user
from ..game_systems.corporations.CorporationHandler import CorporationHandler, UserCRUD, CorporationCRUD

from . import dependency_session, ResponseBuilder, DataName, MyLogger, common_http_errors, AsyncSession
error_log = MyLogger.errors()

corporation_router = APIRouter(
    prefix="/corporations",
    tags=["corporations"],
    responses={404: {"description": "Not Found"}}
)

@corporation_router.post("/create-corporation")
async def create_corporation(
        request: NewCorporationInfo,
        session: AsyncSession = Depends(dependency_session),
        user_id: int = Depends(current_user.ensure_user_exists)
    ):
    corp_manager = CorporationHandler(session)
    try:
        new_corporation = await corp_manager.create_corporation(request, user_id)
        await session.commit()

        await corp_manager.add_user_to_corporation(user_id, new_corporation.id)
        await session.commit()
        msg = f"{request.name} created successfully!"
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@corporation_router.post("/add-user")
async def add_user_to_corporation(
        user_id_to_add: int,
        corp_id: int,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        corp_manager = CorporationHandler(session)
        await corp_manager.check_if_user_is_leader(corp_id, user_id)
        if user_id_to_add == user_id:
            raise ValueError("You can't add yourself!")
        msg = await corp_manager.add_user_to_corporation(user_id_to_add, corp_id)
        await session.commit()
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@corporation_router.post("/remove-user")
async def remove_user_from_corporation(
        user_id_to_remove: int,
        corp_id: int,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        corp_manager = CorporationHandler(session)
        await corp_manager.check_if_user_is_leader(user_id, corp_id)
        if user_id_to_remove == user_id:
            raise ValueError("Cannot remove yourself, disband the Corporation first")

        msg = await corp_manager.remove_player_from_corporation(user_id_to_remove, corp_id)
        await session.commit()
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


