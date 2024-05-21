from ..job_schema import JobTypes, JobCreate
from ..education_schema import EducationPaths


general_jobs_data = [
    {
        "job_type": JobTypes.General,
        "job_name": "Store Bagger",
        "description": "Bag groceries at the store.",
        "chance_for_promotion": 2.5,
        "chance_to_fail": 1,
        "energy_required": 5,
        "level_required": 1,
        "reputation_required": 0,
        "education_required": EducationPaths.CommunityCollege.value,
        "education_progress_required": 0.00,
        "income": 40,
        "level_adj": 0.25,
        "chance_for_promo_adj": 0.25,
        "reputation_adj": 0.00,
    },
    {
        "job_type": JobTypes.General,
        "job_name": "Cook",
        "description": "Flip paddies at McPaddies.",
        "chance_for_promotion": 2.5,
        "chance_to_fail": 1,
        "energy_required": 6,
        "level_required": 3,
        "reputation_required": 0,
        "education_required": None,
        "education_progress_required": 0.00,
        "income": 60,
        "level_adj": 0.25,
        "chance_for_promo_adj": 0.25,
        "reputation_adj": 0.00,
    },
]

general_jobs_list = [JobCreate(**job) for job in general_jobs_data]
