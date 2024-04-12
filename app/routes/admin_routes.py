from fastapi import APIRouter, HTTPException, Depends, Form, status
from sqlmodel import Session, select
from pydantic import BaseModel, parse_obj_as
from typing import Optional, Union
from enum import Enum
from ..models.models import User
from ..models.other_models import Jobs
from ..models.item_models import Items, ItemType, ItemQuality, FoodItems, Weapon, IndustrialCraftingRecipes
from ..auth.auth_handler import get_current_user
from ..services.job_service import create_job, JOB_TYPES
from ..database.UserCRUD import engine
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

        example_data = {
            'job_name': 'Store Bagger',
            "job_type": 'General',
            "income": 40,
            "energy_required": 5,
            "description": "Bag Groceries at the store",
            "required_stats": '{"level": 1}',
            "stat_changes": '{"level": 1}'
        }

        if job_data["job_type"] not in JOB_TYPES:
            return f'Job must be in {JOB_TYPES}'

        new_job = create_job(job_data=job_data)
        logger.info(f'ADMIN ACTION: Created new job {new_job.job_name}')
        return f"{new_job.job_name} created successfully."





def item_data_json(item_name: str, illegal: bool, buy_price: int, category: str, quality: str):
    item_data = {"item_name": item_name, "illegal": illegal, "buy_price": buy_price, "category": category, "quality": quality}
    return item_data

class WeaponDetailCreate(BaseModel):
    damage: int
    damage_bonus: Optional[int]
    evasiveness_bonus: Optional[int]
    strength_bonus: Optional[int]
    attachment_one: Optional[str]
    attachment_two: Optional[str]

class FoodItemsCreate(BaseModel):
    health_bonus: int

class IndustrialCraftingCreate(BaseModel):
    item_one: Optional[str]
    item_one_amount: Optional[int]
    item_two: Optional[str]
    item_two_amount: Optional[int]
    item_three: Optional[str]
    item_three_amount: Optional[int]
    item_produced: Optional[str]

class ItemCreate(BaseModel):
    item_name: str
    illegal: bool
    category: ItemType
    quality: ItemQuality
    buy_price: Optional[int]

class ItemCreateRequest(BaseModel):
    general: ItemCreate
    details: Union[WeaponDetailCreate, FoodItemsCreate, IndustrialCraftingCreate]


async def create_general_item(session: Session, item_data: dict, category: ItemType) -> Items:
    item_data["category"] = category
    item = Items(**item_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@admin_router.post("/create-weapon")
async def create_weapon_endpoint(request: WeaponDetailCreate, item_name: str, illegal: bool, category: ItemType, quality: ItemQuality, buy_price: Optional[int] = None, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    with Session(engine) as session:
        item_data = item_data_json(item_name,illegal, buy_price, category, quality)
        weapon_item = await create_general_item(session, item_data, ItemType.Weapon)
        weapon_detail = Weapon(item_id=weapon_item.id, **request.dict())
        session.add(weapon_detail)
        session.commit()
        return {"message": "Weapon item created successfully.", "item_id": weapon_item.id}


@admin_router.post("/create-food")
async def create_food_endpoint(request: FoodItemsCreate, item_name: str, illegal: bool, category: ItemType, quality: ItemQuality, buy_price: Optional[int] = None, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    with Session(engine) as session:
        item_data = item_data_json(item_name,illegal, buy_price, category, quality)
        food_item = await create_general_item(session, item_data, ItemType.Food)
        food_detail = FoodItems(item_id=food_item.id, **request.dict())
        session.add(food_detail)
        session.commit()
        return {"message": "Food item created successfully.", "item_id": food_item.id}


@admin_router.post("/create-industrial-crafting")
async def create_industrial_crafting_endpoint(request: IndustrialCraftingCreate, item_name: str, illegal: bool, category: ItemType, quality: ItemQuality, buy_price: Optional[int] = None, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    with Session(engine) as session:
        item_data = item_data_json(item_name,illegal, buy_price, category, quality)
        crafting_item = await create_general_item(session, item_data, ItemType.IndustrialCrafting)
        crafting_details = request.dict()
        crafting_details["item_id"] = crafting_item.id
        industrial_crafting_detail = IndustrialCraftingRecipes(**crafting_details)
        session.add(industrial_crafting_detail)
        session.commit()

        return {"message": f"Industrial crafting item '{crafting_item.item_name}' created successfully.", "item_id": crafting_item.id}


