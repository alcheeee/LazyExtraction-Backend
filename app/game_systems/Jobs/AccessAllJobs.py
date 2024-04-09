from app.database.GameplayCRUDS.GeneralJobsCRUD import GeneralJob
from app.database.UserCRUD import user_crud

class JobFactory:
    @staticmethod
    def get_job(job_key: str):
        all_jobs = {
            'Store Bagger': GeneralJob(
                job_name='Store Bagger',
                job_type='General',
                income=100,
                energy_required=3,
                description='Bag groceries at the local market.',
                required_stats={'level': 1},
                stat_changes={'level': 1}),
            '': None,
            '': None}
        return all_jobs.get(job_key)


def work_users_job(user_id: int):
    user = user_crud.get_user_by_id(user_id=user_id)
    if not user:
        return False, "User not found."

    job_key = user.job
    job = JobFactory.get_job(job_key)
    if not job:
        return False, "You don't have that job."
    return job.do_user_job(user_id=user_id)


def update_user_job(user_id: int, job_key: str):
    job = JobFactory.get_job(job_key)
    if not job:
        return False, "Invalid job specified."
    return job.update_user_job(user_id=user_id)




