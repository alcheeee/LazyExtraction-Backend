from fastapi import APIRouter, Depends
from ..schemas import NewCrewInfo
from ..game_systems.crews.crew_handler import CrewHandler
from ..auth import current_user
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    MyLogger,
    common_http_errors
)

error_log = MyLogger.errors()

crew_router = APIRouter(
    prefix="/crews",
    tags=["crews"],
    responses={404: {"description": "Not Found"}}
)


@crew_router.get("/")
async def root():
    return ResponseBuilder.success("Crew routes ready")


@crew_router.post("/create-crew")
async def create_crew(
        request: NewCrewInfo,
        session: AsyncSession = Depends(get_db),
        user_id: int = Depends(current_user.ensure_user_exists)
    ):
    crew_manager = CrewHandler(session)
    try:
        new_crew = await crew_manager.create_crew(request, user_id)
        await session.commit()

        await crew_manager.add_user_to_crew(user_id, new_crew.id)
        await session.commit()
        msg = f"{request.name} created successfully!"
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@crew_router.post("/add-user")
async def add_user_to_crew(
        user_id_to_add: int,
        crew_id: int,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
    ):
    try:
        crew_manager = CrewHandler(session)
        await crew_manager.check_if_user_is_leader(crew_id, user_id)
        if user_id_to_add == user_id:
            raise ValueError("You can't add yourself!")
        msg = await crew_manager.add_user_to_crew(user_id_to_add, crew_id)
        await session.commit()
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@crew_router.post("/remove-user")
async def remove_user_from_crew(
        user_id_to_remove: int,
        crew_id: int,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
    ):
    try:
        crew_manager = CrewHandler(session)
        await crew_manager.check_if_user_is_leader(user_id, crew_id)
        if user_id_to_remove == user_id:
            raise ValueError("Cannot remove yourself, disband the Crew first")

        msg = await crew_manager.remove_player_from_crew(user_id_to_remove, crew_id)
        await session.commit()
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()
