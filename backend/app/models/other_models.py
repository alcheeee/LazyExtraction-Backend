from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Enum, Relationship
from app.schemas import JobTypes


class Jobs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    job_type: JobTypes = Field(index=True)
    job_name: str = Field(index=True)
    description: str = Field(default="Just a way to earn money")

    chance_for_promotion: float = Field(default=1.00)
    chance_to_fail: int = Field(default=0)

    # Required Stats
    energy_required: int = Field(default=5)
    level_required: int = Field(default=0)
    reputation_required: float = Field(default=0.00)
    training_required: Optional[str] = Field(default=None)
    training_progress_required: Optional[int] = Field(default=0)

    # Rewards
    income: int = Field(default=40)
    level_adj: float = Field(default=0.25)
    chance_for_promo_adj: float = Field(default=0.25)
    reputation_adj: float = Field(default=0.00)



