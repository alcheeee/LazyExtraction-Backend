from fastapi import APIRouter, Depends
from app.game_systems.jobs.job_handler import JobService
from app.game_systems.game_world.room_generator import RoomGenerator
from app.game_systems.game_world.world_interactions import InteractionHandler
from app.auth import AccessTokenBearer
from app.crud import UserInventoryCRUD
from app.schemas import (
    JobRequest,
    WorldNames,
    RoomInteraction,
    InteractionTypes
)
from . import (
    DataName,
    AsyncSession,
    ResponseBuilder,
    MyLogger,
    CommonHTTPErrors,
    exception_decorator
)
from app.dependencies.get_db import get_db

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
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    # TODO : Remove Blocking I/O Operations
    user_id = int(user_data['user']['user_id'])
    generator = RoomGenerator(request)
    new_raid = await generator.assign_room_to_user(user_id, session)
    await session.commit()

    new_raid['skill-adjustments'] = {
        "level-adjustment": 0.1,
        "knowledge-adjustment": 0.1
    }
    return ResponseBuilder.success("Entered a raid", DataName.RoomData, new_raid)


@game_router.post("/interaction")
@exception_decorator
async def world_interaction(
        request: RoomInteraction,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    # TODO : Remove Blocking I/O Operations
    user_id = int(user_data['user']['user_id'])
    handler = InteractionHandler(session, user_id)
    msg, data = await handler.handle(request)


    response = ResponseBuilder.success(message=msg, data_name=DataName.RoomData, data=data)
    await session.commit()
    return response



@game_router.post("/job-action")
@exception_decorator
async def job_actions(
        request: JobRequest,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    user_id = int(user_data['user']['user_id'])

    job_handler = JobService(request, user_id, session)
    msg = await job_handler.handle_job_action()
    await session.commit()
    return ResponseBuilder.success(msg)

