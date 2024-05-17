from fastapi import APIRouter, Depends
from .router_ids import RouteIDs
from ..auth.auth_handler import current_user
from ..game_systems.jobs.JobHandler import JobService, JobRequest
from ..game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler

from . import dependency_session, ResponseBuilder, MyLogger, common_http_errors, AsyncSession
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


@game_router.post("/job-action")
async def job_actions(
        request: JobRequest,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        job_handler = JobService(request, user_id, session)
        msg = await job_handler.handle_job_action()
        await session.commit()
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        error_log.error(str(e))
        await session.rollback()
        raise common_http_errors.server_error()



