from fastapi import APIRouter, HTTPException, Depends
from ..models.models import User
from ..models.corp_models import Corporation
from ..services.RaiseHTTPErrors import common_http_errors
from ..schemas.corporation_schema import NewCorporationInfo
from ..auth.auth_handler import get_current_user, current_user
from ..database.db import get_session
from ..game_systems.corporations.CorporationHandler import CorporationHandler, UserCRUD, CorporationCRUD
from ..utils.logger import MyLogger
error_log = MyLogger.errors()

corporation_router = APIRouter(
    prefix="/corporations",
    tags=["corporations"],
    responses={404: {"description": "Not Found"}}
)

@corporation_router.post("/create-corporation")
async def create_corporation(request: NewCorporationInfo, user_id: int = Depends(current_user.ensure_user_exists)):
    async with get_session() as session:
        corp_manager = CorporationHandler(session)
        try:
            new_corporation = await corp_manager.create_corporation(request, user_id)
            await session.commit()

            await corp_manager.add_user_to_corporation(user_id, new_corporation.id)
            await session.commit()
            return {"message": f"{request.name} created successfully!"}

        except ValueError as e:
            await session.rollback()
            raise common_http_errors.mechanics_error(str(e))
        except Exception as e:
            await session.rollback()
            error_log.error(str(e))
            raise common_http_errors.server_error()


@corporation_router.post("/add-user")
async def add_user_to_corporation(user_id_to_add: int, corp_id: int, user_id: int = Depends(current_user.ensure_user_exists)):
    async with get_session() as session:
        try:
            corp_manager = CorporationHandler(session)
            await corp_manager.check_if_user_is_leader(corp_id, user_id)
            result = await corp_manager.add_user_to_corporation(user_id_to_add, corp_id)
            await session.commit()
            return {"message": result}
        except ValueError as e:
            await session.rollback()
            raise common_http_errors.mechanics_error(str(e))
        except Exception as e:
            await session.rollback()
            error_log.error(str(e))
            raise common_http_errors.server_error()


@corporation_router.post("/remove-user")
async def remove_user_from_corporation(user_id_to_remove: int, corp_id: int, user_id: int = Depends(current_user.ensure_user_exists)):
    async with get_session() as session:
        try:
            corp_manager = CorporationHandler(session)
            await corp_manager.check_if_user_is_leader(user_id, corp_id)
            if user_id_to_remove == user_id:
                raise ValueError("Cannot remove yourself, disband the Corporation first")

            result = await corp_manager.remove_player_from_corporation(user_id_to_remove, corp_id)
            await session.commit()
            return {"message": result}

        except ValueError as e:
            await session.rollback()
            raise common_http_errors.mechanics_error(str(e))
        except Exception as e:
            await session.rollback()
            error_log.error(str(e))
            raise common_http_errors.server_error()


