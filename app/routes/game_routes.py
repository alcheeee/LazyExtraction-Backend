from pydantic import BaseModel
from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends, status

from ..database.db import get_session
from .router_ids import RouteIDs
from .auth_routes import user_router
from ..models.models import User, Inventory, InventoryItem
from ..models.item_models import Items
from ..auth.auth_handler import get_current_user
from ..services.job_service import job_service
from app.game_systems.items.ItemStatsHandlerCRUD import ItemStatsHandler
from app.game_systems.gameplay_options import equipment_map
from app.utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()


game_router = APIRouter(
    prefix="/game",
    tags=["game"],
    responses={404: {"description": "Not Found"}}
)


class UserItemActionRequest(BaseModel):
    item_id: int

@game_router.post("/equip-item")
async def equip_unequip_inventory_item(request: UserItemActionRequest, user: User = Depends(get_current_user)):
    try:
        result = ItemStatsHandler(user.id, request.item_id).user_equip_unequip_item()
        if result in ["equipped", "unequipped"]:
            return {"message": f"Item {result}"}
        else:
            return HTTPException(status_code=400, detail={"message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})



class UserActionRequest(BaseModel):
    button_id: str

@game_router.post("/specific-user-action")
async def user_action_buttons(request: UserActionRequest, user: User = Depends(get_current_user)):
    try:
        route_id = RouteIDs(request.button_id, user)
        msg = route_id.find_id()
        return {"message": msg}
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})


@game_router.get("/get-all-jobs")
async def get_all_job_info(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    try:
        result = job_service.get_all_jobs(session)
        if result:
            return result
        else:
            return HTTPException(status_code=400, detail={"message": "Internal error occured"})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})


class UserApplyJobRequest(BaseModel):
    job_name: str

@game_router.post("/apply-to-job")
async def apply_to_job(request: UserApplyJobRequest, user: User = Depends(get_current_user)):
    try:
        result = job_service.update_user_job(user.id, request.job_name),
        return {"message": result}

    except ValueError as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})



