from fastapi import APIRouter, Depends
from ..game_systems.items.item_stats_handler import ItemStatsHandler
from ..auth import AccessTokenBearer
from ..crud import UserInventoryCRUD
from ..schemas import (
    StashStatusSwitchRequest,
    EquippingUnequippingRequest
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


inventory_router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)


@inventory_router.get("/")
async def root():
    return ResponseBuilder.success("Inventory routes ready")


@inventory_router.post("/equip-item")
@exception_decorator
async def equip_inventory_item(
        request: EquippingUnequippingRequest,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    user_id = int(user_data['user']['user_id'])

    item_stats_handler = ItemStatsHandler(user_id, request.inventory_item_id, session)
    result = await item_stats_handler.equip_item()
    await session.commit()
    return ResponseBuilder.success(f"Item {result}")


@inventory_router.post("/unequip-item")
@exception_decorator
async def unequip_inventory_item(
        request: EquippingUnequippingRequest,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    user_id = int(user_data['user']['user_id'])

    item_stats_handler = ItemStatsHandler(user_id, request.inventory_item_id, session)
    result = await item_stats_handler.unequip_item()
    await session.commit()
    return ResponseBuilder.success(f"Item {result}")


@inventory_router.post("/item-stash-status")
@exception_decorator
async def change_stash_status(
        request: StashStatusSwitchRequest,
        user_data: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_db)
):
    user_id = int(user_data['user']['user_id'])
    if request.quantity <= 0:
        raise ValueError("Invalid quantity to move")

    inv_crud = UserInventoryCRUD(None, session)
    await inv_crud.switch_item_stash_status(user_id, request.inventory_item_id, request.to_stash, request.quantity)
    await session.commit()
    return ResponseBuilder.success("Item transferred")
