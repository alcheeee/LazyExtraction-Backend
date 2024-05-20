from typing import Optional
from pydantic import BaseModel
from enum import Enum


class JobTypes(str, Enum):
    General = "general"
    Criminal = "criminal"
    CriminalJustice = "criminal_justice"
    Economics = "economics"
    MilitaryPlanning = "military_planning"
    Engineering = "engineer"
    HealthScience = "health_science"
    ComputerScience = "computer_science"


class JobActionType(str, Enum):
    Work = "work"
    Apply = "apply"
    Quit = "quit"
    AskForPromo = "ask_for_promo"


class JobRequest(BaseModel):
    job_action: JobActionType = JobActionType.Work
    job_name: Optional[str]


class JobCreate(BaseModel):
    job_type: JobTypes
    job_name: str
    description: str

    chance_for_promotion: float = 2.00  # If Promotion, increase other stats by x
    chance_to_fail: int = 0  # If failed, remove chance_for_promotion

    # Required Stats
    energy_required: int = 5
    level_required: int = 1
    reputation_required: float = 0.00
    education_required: Optional[str] = None
    education_progress_required: float = 0.00

    # Rewards
    income: int = 40
    level_adj: float = 0.25
    chance_for_promo_adj: float = 0.25
    reputation_adj: float = 0.00


class JobRequirementsCheck:
    user_stats_to_check = {
        "energy_required": "energy",
        "level_required": "level",
        "reputation_required": "reputation"
    }
    user_education_to_check = {
        #"education_required": "education", # We don't fetch this, since this will be used for something else
        "education_progress_required": ""
        # We fetch this dynamically depending on education_required and EducationPaths

    }
