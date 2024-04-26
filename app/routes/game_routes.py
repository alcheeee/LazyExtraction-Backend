from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends
from ..database.db import get_session
from .router_ids import RouteIDs
from ..models.models import User
from ..auth.auth_handler import get_current_user
from ..services.job_service import job_service
from app.game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler
from app.utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()


game_router = APIRouter(
    prefix="/game",
    tags=["game"]
)


@game_router.post("/equip-item/{item_id:int}")
async def equip_unequip_inventory_item(item_id: int,
                                       user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            item_stats_handler = ItemStatsHandler(user.id, item_id, session)
            result = await item_stats_handler.user_equip_unequip_item()

            await session.commit()
            return {"message": f"Item {result}"}
        except ValueError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail={"message": str(e)})
        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=500, detail={"message": "Internal error"})


@game_router.post("/specific-user-action/{button_name}")
async def user_action_buttons(button_name: str, user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            session.add(user)
            route_id = RouteIDs(button_name, user, session=session)
            msg = await route_id.find_id()
            return {"message": msg}

        except ValueError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail={"message": str(e)})
        except Exception as e:
            await session.rollback()
            admin_log.error(str(e))
            raise HTTPException(status_code=500, detail={"message": "Internal Error"})


@game_router.get("/get-all-jobs")
async def get_all_job_info(user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            result = await job_service.get_all_jobs(session)
            return result

        except Exception as e:
            admin_log.error(str(e))
            raise HTTPException(status_code=500, detail={"message": "Internal error"})


@game_router.post("/apply-to-job/{job_name}")
async def apply_to_job(job_name: str, user: User = Depends(get_current_user)):
    async with get_session() as session:
        try:
            session.add(user)
            result = await job_service.update_user_job(user, job_name, session=session),
            return {"message": result}
        except ValueError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail={"message": str(e)})
        except Exception as e:
            admin_log.error(str(e))
            raise HTTPException(status_code=500, detail={"message": "Internal Error"})



