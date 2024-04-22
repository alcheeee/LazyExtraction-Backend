from fastapi import APIRouter, HTTPException, Depends, Form
from sqlmodel import Session, select
from pydantic import BaseModel
from ..game_systems.items.ItemCRUD import create_item
from ..game_systems.items.ItemCreationLogic import WeaponDetailCreate, ClothingDetailCreate, ItemCreate
from ..game_systems.markets.MarketHandlerCRUD import BackendMarketHandler
from ..models.models import User
from ..models.other_models import Jobs
from ..game_systems.gameplay_options import ItemQuality
from ..auth.auth_handler import get_current_user
from ..services.job_service import create_job, JOB_TYPES
from ..database.UserCRUD import user_crud
from ..database.db import get_session
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
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})

    with Session(engine) as session:
        transaction = session.begin()
        try:
            db_job = session.exec(select(Jobs).where(Jobs.job_name == job_name)).first()
            if db_job:
                raise HTTPException(status_code=400, detail={"message": "Job already created!"})

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
async def create_weapon_endpoint(request: WeaponDetailCreate,
                                 session: Session = Depends(get_session),
                                 user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})

    result, msg = create_item("Weapon", user.id, request, session)
    if not result:
        raise HTTPException(status_code=400, detail={"message": msg})

    admin_log.info(f"ADMIN {user.id} - Created {request.item_name}.")
    return {"message": msg}

@admin_router.post("/create-item/clothing")
async def create_clothing_endpoint(request: ClothingDetailCreate,
                                   session: Session = Depends(get_session),
                                   user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})

    result, msg = create_item("Clothing", user.id, request, session)
    if not result:
        raise HTTPException(status_code=400, detail={"message": msg})

    admin_log.info(f"ADMIN {user.id} - Created {request.item_name}.")
    return {"message": msg}



class MarketItemAdd(BaseModel):
    item_id: int
    market_name: str
    item_cost: int
    sell_price: int


@admin_router.post("/add-item-to-market")
async def add_item_to_market(m_item: MarketItemAdd, user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})
    market_handler = BackendMarketHandler(m_item.item_id, m_item.market_name, m_item.item_cost, m_item.sell_price)
    result = market_handler.add_item_to_market()
    if not result:
        raise HTTPException(status_code=400, detail="Failed to add item to market")

    return {"message": f"Added {m_item.item_id} to {m_item.market_name}"}


@admin_router.post("/add-item-to-user/{username}/{item_id}/{quantity}")
async def add_an_item_to_user(username: str,item_id: int,quantity: int,
                              session: Session = Depends(get_session),
                              user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail={"message": "Insufficient permissions"})

    user_sending = session.exec(select(User).where(User.username == username)).one_or_none()
    if not user_sending:
        raise HTTPException(status_code=400, detail={"message": f"Couldn't find user."})

    try:
        user_crud.update_user_inventory(user_sending.id, item_id, quantity, session)
        session.commit()
        return {"message": f"Added {quantity} of item {item_id} to {user_sending.username}"}
    except Exception as e:
        session.rollback()
        admin_log.error(str(e))
        raise HTTPException(status_code=500, detail={"message": f"Server error"})
