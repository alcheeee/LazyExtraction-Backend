from fastapi import APIRouter, HTTPException, Depends
from .router_ids import RouteIDs
from ..models.models import User
from ..auth.auth_handler import current_user
from ..services.job_service import job_service
from ..game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler

from . import dependency_session, ResponseBuilder, DataName, MyLogger, common_http_errors, AsyncSession
error_log = MyLogger.errors()
game_log = MyLogger.game()


game_router = APIRouter(
    prefix="/game",
    tags=["game"]
)


@game_router.post("/equip-item/{item_id:int}")
async def equip_unequip_inventory_item(
        item_id: int,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        item_stats_handler = ItemStatsHandler(user_id, item_id, session)
        result = await item_stats_handler.user_equip_unequip_item()
        await session.commit()
        return ResponseBuilder.success(f"Item {result}")

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        error_log.error(str(e))
        await session.rollback()
        raise common_http_errors.server_error()


@game_router.post("/specific-user-action/{button_name}")
async def user_action_buttons(
        button_name: str,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        session.add(user)
        route_id = RouteIDs(button_name, user_id, session=session)
        msg = await route_id.find_id()
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        error_log.error(str(e))
        await session.rollback()
        raise common_http_errors.server_error()


@game_router.get("/get-all-jobs")
async def get_all_job_info(
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        result = await job_service.get_all_jobs(session)
        return result

    except Exception as e:
        error_log.error(str(e))
        raise common_http_errors.server_error()


@game_router.post("/apply-to-job/{job_name}")
async def apply_to_job(
        job_name: str,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        msg = await job_service.update_user_job(user_id, job_name, session=session),
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        error_log.error(str(e))
        await session.rollback()
        raise common_http_errors.server_error()



