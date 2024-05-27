from fastapi import APIRouter, Depends
from ..game_systems.jobs.JobHandler import JobService
from ..game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler
from ..game_systems.game_world.world_handler import CreateNodeWorld, RoomGenerator
from ..auth import current_user
from ..config import settings
from ..schemas import (
    JobRequest,
    WorldNames,
    WorldTier,
    WorldCreator,
    RoomInteraction
)
from . import (
    AsyncSession,
    dependency_session,
    ResponseBuilder,
    MyLogger,
    common_http_errors
)

error_log = MyLogger.errors()
game_log = MyLogger.game()

game_router = APIRouter(
    prefix="/game",
    tags=["game"]
)


@game_router.put("/new-world")
async def create_new_world(
        world_name: WorldNames,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
):
    try:
        if settings.USE_NODE_SYSTEM:
            world_data = WorldCreator(
                world_name=world_name,
                world_tier=WorldTier.Tier1,
                node_json=''
            )
            create_user_world = CreateNodeWorld(world_data, user_id, session)
            new_world = await create_user_world.create_world()

            session.add(new_world)
            await session.commit()
            await session.refresh(new_world)
            return new_world
        else:
            pass

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))

    except Exception as e:
        error_log.error(str(e))
        await session.rollback()
        raise common_http_errors.server_error()


@game_router.put("/interaction")
async def current_interaction(
        interaction: RoomInteraction,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
):
    try:
        pass

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))

    except Exception as e:
        error_log.error(str(e))
        await session.rollback()
        raise common_http_errors.server_error()


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



