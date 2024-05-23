from pydantic import BaseModel
from enum import Enum


class TrainingPaths(str, Enum):
    BasicTraining = "basic_training"
    AdvancedInfantry = "advanced_infantry"
    SpecialOperations = "special_operations"
    Intelligence = "intelligence"
    Engineering = "engineering"
    Medical = "medical"
    Leadership = "leadership"
    Economics = "economics"


