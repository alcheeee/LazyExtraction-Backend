from pydantic import BaseModel
from enum import Enum


class EducationPaths(str, Enum):
    CommunityCollege = "community_college"  # Increase Knowledge/Intelligence
    CriminalJustice = "criminal_justice"  # Required for Criminal Justice field
    Economics = "economics"
    MilitaryPlanning = "military_planning"
    Engineering = "engineer"
    HealthScience = "health_science"
    ComputerScience = "computer_science"


class CJEducation(BaseModel):
    pass


class CCEducation(BaseModel):
    pass
