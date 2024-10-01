# TODO : Combat within range for now
#  Get users weapon, estimate range of damage on target,
#  allow front-end to calculate, verify within the a plausible range of values.
#  The point is to reduce load on the backend, and if there is a problem with cheating,
#  I will have the resources to find a better solution

from fastapi import APIRouter, Depends
from app.auth import AccessTokenBearer

from app.game_systems.items.weapons.attachment_handler import WeaponAttachmentsHandler
from app.schemas.weapon_schemas import (
    AttachmentTypes,
    AddAttachmentsRequest,
    RemoveAttachmentRequest
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
    weapon_handler = WeaponAttachmentsHandler(
        session, user_id, request.weapon_inventory_id
    )
    data = await weapon_handler.build_weapon(
        request.attachments_to_add
    )
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
    weapon_handler = WeaponAttachmentsHandler(
        session, user_id, request.weapon_inventory_id
    )
    data = await weapon_handler.remove_attachments(
        request.attachments_to_remove
    )
    await session.commit()
    return ResponseBuilder.success("Attachments Removed", data_name=DataName.WeaponData, data=data)
