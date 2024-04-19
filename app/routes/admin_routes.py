from fastapi import APIRouter, HTTPException, Depends, Form, status
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Union
from ..game_systems.items.ItemCRUD import create_item
from ..game_systems.items.ItemCreationLogic import WeaponDetailCreate, ClothingDetailCreate, FoodDetailCreate, IndustrialCraftingCreate, ItemCreate
from ..game_systems.markets.MarketHandlerCRUD import BackendMarketHandler
from ..models.models import User
from ..models.other_models import Jobs
from ..game_systems.gameplay_options import ItemQuality
from ..auth.auth_handler import get_current_user
from ..services.job_service import create_job, JOB_TYPES
from ..database.UserCRUD import engine, user_crud
from ..utils.logger import MyLogger
user_log = MyLogger.user()
admin_log = MyLogger.admin()
game_log = MyLogger.game()

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
        admin_log.warning(f"{user} made an admin request!")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message": "Insufficient permissions"})

    with Session(engine) as session:
        transaction = session.begin()
        try:
            db_job = session.exec(select(Jobs).where(Jobs.job_name == job_name)).first()
            if db_job:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Job already created!"})

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
                return {"message": f'Job must be in {JOB_TYPES}'}

            new_job = create_job(job_data=job_data)
            admin_log.info(f'ADMIN {user.id} - Created new job {new_job.job_name}')
            return {"message": f"{new_job.job_name} created successfully."}

        except Exception as e:
            session.rollback()
            admin_log.error(str(e))
            return {"message": "An error occured"}


@admin_router.post("/create-item/weapon")
async def create_weapon_endpoint(request: WeaponDetailCreate, item_name: str, illegal: bool, random_generate_quality: bool, quality: ItemQuality, quantity: int, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})

    item_type = "Weapon"
    result, msg = create_item(item_type, user.id, request, item_name, illegal,
                              random_generate_quality,
                              quality, quantity)
    msg = {"message": msg}
    if result:
        admin_log.info(f"ADMIN {user.id} - Created {item_name}.")
        return msg
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@admin_router.post("/create-item/food")
async def create_food_endpoint(request: FoodDetailCreate, item_name: str, illegal: bool, random_generate_quality: bool, quality: ItemQuality, quantity: int, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})

    item_type = "Food"
    result, msg = create_item(item_type, user.id, request, item_name, illegal,
                              random_generate_quality,
                              quality, quantity)
    msg = {"message": msg}
    if result:
        admin_log.info(f"ADMIN {user.id} - Created {item_name}.")
        return msg
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@admin_router.post("/create-item/clothing")
async def create_clothing_endpoint(request: ClothingDetailCreate, item_name: str, illegal: bool, random_generate_quality: bool, quality: ItemQuality, quantity: int, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})

    item_type = "Clothing"
    result, msg = create_item(item_type, user.id, request, item_name, illegal,
                              random_generate_quality,
                              quality, quantity)
    msg = {"message": msg}
    if result:
        admin_log.info(f"ADMIN {user.id} - Created {item_name}.")
        return msg
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@admin_router.post("/create-item/industrial-crafting")
async def create_industrial_crafting_endpoint(request: IndustrialCraftingCreate, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})

    item_type = "IndustrialCrafting"
    result = False
    """
    TODO - ADD CRAFTING LOGIC
    """
    msg = {"message": ""}

    if result:
        return msg
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@admin_router.post("/add-item-to-market")
async def add_item_to_market(item_id: int, market_name: str, item_cost: int, sell_price: int, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})
    result = BackendMarketHandler(item_id, market_name, item_cost, sell_price).add_item_to_market()
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Invalid Request"})
    return {"message": f"Added {item_id} to {market_name}"}


@admin_router.post("/add-item-to-user")
async def add_an_item_to_user(username: str, item_id: int, quantity: int, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})

    with Session(engine) as session:
        user_sending = session.exec(select(User).where(User.username == username)).first()
        if user_sending:
            user_crud.update_user_inventory(user_sending.id, item_id, quantity, session=session)
            session.commit()
            return {"message": f"Added item to {user_sending.username}"}
        else:
            msg = {"message": f"Couldn't find user."}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

