from sqlmodel import select
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from ..models.models import User
from ..models.corp_models import Corporation
from ..auth.auth_handler import get_current_user
from ..database.db import get_session
from ..game_systems.corporations.CorporationCRUD import CorpManager
from ..utils.logger import MyLogger
admin_log = MyLogger.admin()

corporation_router = APIRouter(
    prefix="/corporations",
    tags=["corporations"],
    responses={404: {"description": "Not Found"}}
)


@corporation_router.post("/create-corporation/{name:str}/{type:str}")
async def create_corporation(name: str, type: str, user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            corp_manager = CorpManager(session)
            result = await corp_manager.create_corporation(name, type, user.id)
            return {"message": result}

        except ValueError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail={"message": str(e)})
        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=500, detail={"message": "Error creating Corporation"})


@corporation_router.post("/add-user/{user_id_to_add:int}")
async def add_user_to_corporation(user_id_to_add: int, user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            corp_manager = CorpManager(session)
            corporation = await session.get(Corporation, user.corp_id)

            if not corporation:
                raise HTTPException(status_code=404, detail="No associated corporation found.")
            if user.username != corporation.leader:
                raise HTTPException(status_code=403, detail="You are not authorized to add users.")

            target_user = await session.get(User, user_id_to_add)
            if not target_user:
                raise HTTPException(status_code=404, detail="User not found.")

            success, msg = await corp_manager.add_user_to_corporation(user_id_to_add, user.corp_id)
            if not success:
                raise HTTPException(status_code=400, detail=msg)
            return {"message": msg}

        except ValueError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail={"message": str(e)})
        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=500, detail={"message": "Internal Error"})

@corporation_router.post("/remove-user/{user_id_to_remove:int}")
async def remove_user_from_corporation(user_id_to_remove: int, user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            corp_manage = CorpManager(session)
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
            admin_log.error(str(e))
            raise HTTPException(status_code=500, detail={"message": "Internal Error"})


