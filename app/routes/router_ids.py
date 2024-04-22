from ..database.UserCRUD import user_crud
from ..services.job_service import job_service

class RouteIDs:
    def __init__(self, route_name_id, user):
        self.route_name_id = route_name_id
        self.user = user

    def find_id(self):
        try:
            actions = {
                "work-job": lambda: job_service.do_user_job(self.user.id, self.user.job),
                "quit-job": lambda: job_service.update_user_job(self.user.id, 'quit'),
            }

            if self.route_name_id in actions:
                msg = actions[self.route_name_id]()
                return {"message": msg}
            else:
                raise ValueError("Invalid request")

        except ValueError as e:
            return {"message": str(e)}