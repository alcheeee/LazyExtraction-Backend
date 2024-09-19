# TODO : Combat within range for now
#  Get users weapon, estimate range of damage on target,
#  allow front-end to calculate, verify within the a plausible range of values.
#  The point is to reduce load on the backend, and if there is a problem with cheating,
#  I will have the resources to find a better solution

from fastapi import APIRouter, Depends
from ..auth import AccessTokenBearer

from ..game_systems.items.weapons.attachment_handler import WeaponStatsHandler
from ..schemas.weapon_schemas import (
    AttachmentTypes,
    AddAttachmentsRequest,
    RemoveAttachmentRequest
)
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    DataName,
    MyLogger,
    CommonHTTPErrors,
    exception_decorator
)

error_log = MyLogger.errors()
game_log = MyLogger.game()

combat_router = APIRouter(
    prefix="/combat",
    tags=["combat"]
)


@combat_router.get("/")
async def root():
    return ResponseBuilder.success("Combat router ready")


@combat_router.post("/build-weapon")
@exception_decorator
async def build_weapon(
        request: AddAttachmentsRequest,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    user_id = int(user_data['user']['user_id'])
    weapon_handler = WeaponStatsHandler(
        session, user_id, request.weapon_inventory_id
    )
    weapon_item, updated_weapon = await weapon_handler.apply_attachments(
        request.attachments_to_add
    )
    effective_stats = weapon_handler.calculate_effective_stats(
        weapon_item.weapon_details, updated_weapon.modifications
    )
    data = {
        "weapon_name": weapon_item.item_name,
        "modifications": updated_weapon.modifications,
        "effective-stats": effective_stats
    }
    await session.commit()
    return ResponseBuilder.success("Weapon built", data_name=DataName.WeaponData, data=data)


@combat_router.post("/remove-attachment")
@exception_decorator
async def remove_attachment(
        request: RemoveAttachmentRequest,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    user_id = int(user_data['user']['user_id'])
    weapon_handler = WeaponStatsHandler(
        session, user_id, request.weapon_inventory_id
    )
    weapon_item, updated_weapon = await weapon_handler.remove_attachments(
        request.attachments_to_remove
    )

    effective_stats = weapon_handler.calculate_effective_stats(
        weapon_item.weapon_details, updated_weapon.modifications  # type: ignore
    )
    data = {
        "weapon_name": weapon_item.item_name,
        "modifications": updated_weapon.modifications,
        "effective-stats": effective_stats
    }
    await session.commit()
    return ResponseBuilder.success("Attachments Removed", data_name=DataName.WeaponData, data=data)
