from fastapi import APIRouter, Depends
from ..auth import current_user
from ..crud import UserInventoryCRUD, UserCRUD
from . import (
    AsyncSession,
    dependency_session,
    ResponseBuilder,
    DataName,
    MyLogger,
    common_http_errors
)
from ..schemas.item_schema import (
    ClothingCreate,
    ArmorCreate,
    WeaponCreate
)
from ..game_systems.items.ItemHandler import (
    ClothingCreator,
    WeaponCreator,
    ArmorCreator
)
from ..models import (
    User,
    Inventory
)

error_log = MyLogger.errors()
admin_log = MyLogger.admin()


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not Found"}}
)


@admin_router.post("/create-item/clothing")
async def create_clothing_item_endpoint(
        request: ClothingCreate,
        admin_username: str = Depends(current_user.check_if_admin),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        clothing_creator = ClothingCreator(request=request, session=session)
        response_json = await clothing_creator.create_clothing_item()
        await session.commit()

        msg = f"Admin {admin_username} created clothing item {request.item_name}"
        admin_log.info(msg)
        return ResponseBuilder.success(msg, DataName.ItemDetails, response_json)

    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@admin_router.post("/create-item/armor")
async def create_armor_item_endpoint(
        request: ArmorCreate,
        admin_username: str = Depends(current_user.check_if_admin),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        armor_creator = ArmorCreator(request=request, session=session)
        response_json = await armor_creator.create_armor()
        await session.commit()

        msg = f"Admin {admin_username} created armor item {request.item_name}"
        admin_log.info(msg)
        return ResponseBuilder.success(msg, DataName.ItemDetails, response_json)

    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()


@admin_router.post("/create-item/weapon")
async def create_weapon_item_endpoint(
        request: WeaponCreate,
        admin_username: str = Depends(current_user.check_if_admin),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        weapon_creator = WeaponCreator(request=request, session=session)
        response_json = await weapon_creator.create_weapon()
        await session.commit()

        msg = f"Admin {admin_username} created weapon item {request.item_name}"
        admin_log.info(msg)
        return ResponseBuilder.success(msg, DataName.ItemDetails, response_json)

    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()



@admin_router.put("/add-item-to-user/{username}/{item_id}/{quantity}")
async def add_an_item_to_user(
        username: str, item_id: int, quantity: int,
        session: AsyncSession = Depends(dependency_session),
        admin_username: str = Depends(current_user.check_if_admin)
    ):

    user_inventory_crud = UserInventoryCRUD(Inventory, session)
    user_crud = UserCRUD(User, session)
    try:
        receiving_inventory_id = await user_crud.get_user_inventory_id_by_username(username)
        if not receiving_inventory_id:
            raise common_http_errors.server_error()

        result = await user_inventory_crud.update_user_inventory_item(
            inventory_id=receiving_inventory_id,
            item_id=item_id,
            quantity_change=quantity
        )
        await session.commit()
        msg = f"Added/Removed {quantity} of item {item_id} to {username}"
        admin_log.info(msg)
        return ResponseBuilder.success(msg, DataName.ItemGiven, result)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))
    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()





