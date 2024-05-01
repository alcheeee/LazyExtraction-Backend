from ...crud.JobsCRUD import JobsCRUD
from ...models.other_models import Jobs

jobs_list = [
        Jobs(job_name="Store Bagger", job_type="General",
             income=60, energy_required=5,
             description="Bag groceries at the store.",
             required_stats='{"level": 1.00}',
             stat_changes='{"level": 0.25}'),

        Jobs(job_name="Cook", job_type="General",
             income=80, energy_required=5,
             description="Flip paddies at McPaddies.",
             required_stats='{"level": 3.00}',
             stat_changes='{"level": 0.30}')
    ]

async def init_jobs_content(session):
    crud_jobs = JobsCRUD(Jobs, session)
    try:
        for job in jobs_list:
            existing_job = await crud_jobs.get_by_name(job.job_name)
            if not existing_job:
                created_job = await crud_jobs.create(job)
                if created_job:
                    return True
                else:
                    return None
    except Exception as e:
        return None

