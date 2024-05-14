from fastapi import APIRouter, Depends
from ..game_systems.items.ItemHandler import ItemCreator
from ..crud.UserInventoryCRUD import UserInventoryCRUD
from ..crud.UserCRUD import UserCRUD
from ..models.models import User, Inventory
from ..auth.auth_handler import current_user
from ..schemas.item_schema import ItemStats
from ..services.RaiseHTTPErrors import common_http_errors
from ..database.db import get_session
from ..utils.logger import MyLogger
error_log = MyLogger.errors()
admin_log = MyLogger.admin()
game_log = MyLogger.game()


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not Found"}}
)


@admin_router.post("/create-item/equippable")
async def create_equippable_item_endpoint(request: ItemStats,
                                          admin_username: str = Depends(current_user.check_if_admin)):
    async with get_session() as session:
        try:
            item_creator = ItemCreator(item_details=request, session=session)
            response_json = await item_creator.create_item()
            await session.commit()

            msg = f"Admin {admin_username} created item {request.item_name}"
            admin_log.info(msg)
            return {"message": msg, "item-details": response_json}

        except Exception as e:
            await session.rollback()
            error_log.error(str(e))
            raise common_http_errors.server_error()


@admin_router.put("/add-item-to-user/{username}/{item_id}/{quantity}")
async def add_an_item_to_user(username: str, item_id: int, quantity: int,
                              admin_username: str = Depends(current_user.check_if_admin)):
    async with get_session() as session:
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
            return {"message": f"Added/Removed {quantity} of item {item_id} to {username}"}

        except ValueError as e:
            await session.rollback()
            error_log.error(str(e))
            raise common_http_errors.mechanics_error(str(e))
        except Exception as e:
            await session.rollback()
            error_log.error(str(e))
            raise common_http_errors.server_error()





