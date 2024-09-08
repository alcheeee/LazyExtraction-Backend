from fastapi import APIRouter, Depends
from ..game_systems.jobs.job_handler import JobService
from ..game_systems.items.item_stats_handler import ItemStatsHandler
from ..game_systems.game_world.world_handler import RoomGenerator
from ..game_systems.game_world.world_interactions import InteractionHandler
from ..auth import current_user
from ..crud import UserInventoryCRUD
from ..schemas import (
    JobRequest,
    WorldNames,
    RoomInteraction,
    InteractionTypes,
    StashStatusSwitch
)
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    DataName,
    MyLogger,
    common_http_errors,
    exception_decorator
)

error_log = MyLogger.errors()
game_log = MyLogger.game()

game_router = APIRouter(
    prefix="/game",
    tags=["game"]
)


@game_router.get("/")
async def root():
    return ResponseBuilder.success("Game routes ready")


@game_router.post("/new-world")
@exception_decorator
async def create_new_world(
        request: WorldNames,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):
    generator = RoomGenerator(request)
    new_raid = await generator.assign_room_to_user(user_id, session)
    await session.commit()
    return ResponseBuilder.success("Entered a raid", DataName.RoomData, new_raid)


@game_router.post("/interaction")
@exception_decorator
async def world_interaction(
        request: RoomInteraction,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):
    handler = InteractionHandler(session, user_id)
    msg, data = await handler.handle(request)

    response = ResponseBuilder.success(message=msg, data_name=DataName.RoomData, data=data)
    await session.commit()
    return response


@game_router.post("/equip-item")
@exception_decorator
async def equip_unequip_inventory_item(
        request: int,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):
    item_stats_handler = ItemStatsHandler(user_id, request, session)
    result = await item_stats_handler.user_equip_unequip_item()
    await session.commit()
    return ResponseBuilder.success(f"Item {result}")



@game_router.post("/job-action")
@exception_decorator
async def job_actions(
        request: JobRequest,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):
    job_handler = JobService(request, user_id, session)
    msg = await job_handler.handle_job_action()
    await session.commit()
    return ResponseBuilder.success(msg)


@game_router.post("/item-stash-status")
@exception_decorator
async def change_stash_status(
        request: StashStatusSwitch,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):
    inv_crud = UserInventoryCRUD(None, session)
    await inv_crud.switch_item_stash_status(user_id, request.item_id, request.to_stash, request.quantity)
    await session.commit()
    return ResponseBuilder.success("Item transferred")
