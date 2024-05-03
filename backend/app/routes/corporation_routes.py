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
        try:
            corp_manager = CorporationHandler(session)
            new_corporation = await corp_manager.create_corporation(request, user_id)
            await session.commit()
            await corp_manager.add_user_to_corporation(user_id, new_corporation.id)
            await session.commit()
            return {"message": f"{new_corporation.name} created successfully!"}

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
            user_crud = UserCRUD(User, session)
            corp_crud = CorporationCRUD(Corporation, session)
            current_user_username = await user_crud.get_username_by_id(user_id)
            corp_current_leader = await corp_crud.get_corporation_leader(corp_id)

            if not current_user_username or current_user_username != corp_current_leader:
                raise common_http_errors.mechanics_error("You are not authorized to add users")

            result = await corp_manager.add_user_to_corporation(user_id_to_add, corp_id)
            return {"message": msg}

        except ValueError as e:
            await session.rollback()
            raise common_http_errors.mechanics_error(str(e))
        except Exception as e:
            await session.rollback()
            error_log.error(str(e))
            raise common_http_errors.server_error()

@corporation_router.post("/remove-user")
async def remove_user_from_corporation(user_id_to_remove: int, user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            corp_manage = CorporationHandler(session)
            corporation = await session.get(Corporation, user.corp_id)
            if not corporation:
                raise HTTPException(status_code=400, detail={"message": "Invalid Request"})
            if not user.username == corporation.leader:
                raise HTTPException(status_code=403, detail="You are not authorized to remove users.")
            target_user = await session.get(User, user_id_to_remove)
            if not target_user:
                raise HTTPException(status_code=404, detail="User not found.")
            success, msg = await corp_manage.remove_user_from_corporation(user_id_to_remove, user.corp_id)
            if not success:
                raise HTTPException(status_code=400, detail=msg)
            return {"message": msg}

        except ValueError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail={"message": str(e)})
        except Exception as e:
            await session.rollback()
            error_log.error(str(e))
            raise HTTPException(status_code=500, detail={"message": "Internal Error"})


