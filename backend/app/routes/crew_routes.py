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

        username = await crew_manager.get_username(user_id)
        await crew_manager.add_user_to_crew(username, new_crew.id)
        await session.commit()

        return ResponseBuilder.success(f"{request.name} created successfully!")

    except ValueError as e:
        await session.rollback()
        raise common_http_errors.mechanics_error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@crew_router.post("/add-user")
async def add_user_to_crew(
        username_to_add: str,
        crew_id: int,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):
    try:
        crew_manager = CrewHandler(session)
        leader_username = await crew_manager.crew_leader_check(user_id, crew_id)
        if username_to_add == leader_username:
            raise ValueError("You can't add yourself!")
        msg = await crew_manager.add_user_to_crew(username_to_add, crew_id)
        await session.commit()
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        raise common_http_errors.mechanics_error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@crew_router.post("/remove-user")
async def remove_user_from_crew(
        user_to_remove: str,
        crew_id: int,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):
    try:
        crew_manager = CrewHandler(session)
        leader_username = await crew_manager.crew_leader_check(user_id, crew_id)
        if user_to_remove == leader_username:
            raise ValueError("Cannot remove yourself, disband the Crew first")

        msg = await crew_manager.remove_player_from_crew(user_to_remove, crew_id)
        await session.commit()
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        raise common_http_errors.mechanics_error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()
