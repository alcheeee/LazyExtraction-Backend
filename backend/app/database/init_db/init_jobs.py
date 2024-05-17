from ...crud.JobsCRUD import JobsCRUD
from ...models.other_models import Jobs

jobs_list = []

async def init_jobs_content(session):
    crud_jobs = JobsCRUD(Jobs, session)
    try:
        for job in jobs_list:
            existing_job = await crud_jobs.check_name_exists(job.job_name)
            if not existing_job:
                created_job = await crud_jobs.create(job)
                if created_job:
                    return True
                else:
                    return None
    except Exception as e:
        return None

