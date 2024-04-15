from fastapi import APIRouter, HTTPException, Depends, Form, status
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional, Union

from ..game_systems.items.ItemCRUD import create_general_item, create_item, item_data_json
from ..game_systems.items.ItemCreationLogic import WeaponDetailCreate, FoodItemsCreate, IndustrialCraftingCreate, ItemCreate
from ..models.models import User
from ..models.other_models import Jobs
from ..models.item_models import FoodItems, Weapon, IndustrialCraftingRecipes
from ..game_systems.gameplay_options import ItemType, ItemQuality
from ..auth.auth_handler import get_current_user
from ..services.job_service import create_job, JOB_TYPES
from ..database.UserCRUD import engine, user_crud
import logging
from app.utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not Found"}}
)

@admin_router.post("/create-new-job")
async def create_job_endpoint(
    job_name: str = Form(...),
    job_type: str = Form(...),
    income: int = Form(...),
    energy_required: int = Form(...),
    description: str = Form(...),
    required_stats: str = Form(...),
    stat_changes: str = Form(...),
    user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

    with Session(engine) as session:
        db_job = session.exec(select(Jobs).where(Jobs.job_name == job_name)).first()
        if db_job:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job already registered")

        job_data = {
            "job_name": job_name,
            "job_type": job_type,
            "income": income,
            "energy_required": energy_required,
            "description": description,
            "required_stats": required_stats,
            "stat_changes": stat_changes,
        }

        if job_data["job_type"] not in JOB_TYPES:
            return f'Job must be in {JOB_TYPES}'

        new_job = create_job(job_data=job_data)
        logger.info(f'ADMIN ACTION: Created new job {new_job.job_name}')
        return f"{new_job.job_name} created successfully."


class ItemCreateRequest(BaseModel):
    general: ItemCreate
    details: Union[WeaponDetailCreate, FoodItemsCreate, IndustrialCraftingCreate]


@admin_router.post("/create-item/weapon")
async def create_weapon_endpoint(request: WeaponDetailCreate, item_name: str, illegal: bool, random_generate_quality: bool, quality: ItemQuality, quantity: int, buy_price: int, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    item_type = "Weapon"
    result, msg = create_item(item_type, user.id, request, item_name, illegal,
                              random_generate_quality,
                              quality, quantity, buy_price)
    if result:
        logger.info(f"ADMIN {user.id} - Created {item_name}.")
        return msg
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@admin_router.post("/create-item/food")
async def create_food_endpoint(request: FoodItemsCreate, item_name: str, illegal: bool, random_generate_quality: bool, quality: ItemQuality, quantity: int, buy_price: int, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    item_type = "Food"
    result, msg = create_item(item_type, user.id, request, item_name, illegal,
                              random_generate_quality,
                              quality, quantity, buy_price)
    if result:
        logger.info(f"ADMIN {user.id} - Created {item_name}.")
        return msg
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@admin_router.post("/create-item/industrial-crafting")
async def create_industrial_crafting_endpoint(request: IndustrialCraftingCreate, item_name: str, illegal: bool, random_generate_quality: bool, quality: ItemQuality, quantity: int, buy_price: int, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    item_type = "IndustrialCrafting"
    result, msg = create_item(item_type, user.id, request, item_name, illegal,
                              random_generate_quality,
                              quality, quantity, buy_price)
    if result:
        logger.info(f"ADMIN {user.id} - Created {item_name}.")
        return msg
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@admin_router.post("/add-item-to-user")
async def add_an_item_to_user(username: str, item_id: int, quantity: int, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    with Session(engine) as session:
        user_sending = session.exec(select(User).where(User.username == username)).first()
        if user_sending:
            result, msg = user_crud.add_item_to_user_inventory(user_sending.id, item_id, quantity)
            if not result:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
            return msg
        else:
            msg = f"Couldn't find user."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

