from fastapi import APIRouter, Depends
from ..game_systems.jobs.JobHandler import JobService
from ..game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler
from ..game_systems.game_world.world_handler import RoomGenerator
from ..game_systems.game_world.world_interactions import InteractionHandler
from ..auth import current_user
from ..schemas import (
    JobRequest,
    WorldNames,
    WorldTier,
    RoomInteraction,
    InteractionTypes
)
from . import (
    AsyncSession,
    dependency_session,
    ResponseBuilder,
    DataName,
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
        generator = RoomGenerator(world_name, WorldTier.Tier1)
        new_raid = await generator.assign_room_to_user(user_id, session)
        await session.commit()
        return ResponseBuilder.success("Entered a raid", DataName.RoomData, new_raid)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))

    except Exception as e:
        error_log.error(str(e))
        await session.rollback()
        raise common_http_errors.server_error()


@game_router.put("/interaction")
async def world_interaction(
        interaction: RoomInteraction,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
):
    try:
        handler = InteractionHandler(session, user_id)
        msg = await handler.handle(interaction)
        response = ResponseBuilder.success(msg)

        if interaction.action == InteractionTypes.Traverse:
            response = ResponseBuilder.success("New room entered", DataName.RoomData, msg)

        await session.commit()
        return response

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



