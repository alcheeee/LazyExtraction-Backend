from fastapi import APIRouter, HTTPException, Depends, Form, status
from sqlmodel import Session, select
from pydantic import BaseModel
from ..models.models import User, Jobs
from ..auth.auth_handler import oauth2_scheme, get_current_user
from ..services.job_service import create_job, JOB_TYPES
from ..database.UserCRUD import user_crud, engine
import logging
from app.utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

admin_router = APIRouter()

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
    if user.is_admin != 1:
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
            "job_name": "Store Bagger",
            "job_type": "General",
            "income": 150,
            "energy_required": 5,
            "description": "Bag Groceries at the store",
            "required_stats": {"level": 1},
            "stat_changes": {"level": 1}
        }

        if job_data["job_type"] not in JOB_TYPES:
            return f'Job must be in {JOB_TYPES}'

        new_job = create_job(job_data=job_data)
        logger.info(f'ADMIN ACTION: Created new job {new_job.job_name}')
        return f"{new_job.job_name} created successfully."