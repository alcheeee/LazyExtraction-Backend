from typing import Optional
from pydantic import BaseModel
from enum import Enum
from .training_schema import TrainingPaths


class JobTypes(str, Enum):
    Basic = "basic"
    AdvancedInfantry = "advanced_infantry"
    SpecialOperations = "special_operations"
    Intelligence = "intelligence"
    Engineering = "engineering"
    Medical = "medical"
    Leadership = "leadership"
    Economics = "economics"


class JobActionType(str, Enum):
    Work = "work"
    Apply = "apply"
    Quit = "quit"
    AskForPromo = "ask_for_promo"


class JobRequest(BaseModel):
    job_action: JobActionType = JobActionType.Work
    job_name: Optional[str] = "Store Bagger"


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
    training_required: Optional[str] = TrainingPaths.BasicTraining.value
    training_progress_required: float = 0.00

    # Rewards
    income: int = 40
    level_adj: float = 0.25
    chance_for_promo_adj: float = 0.25
    reputation_adj: float = 0.00

