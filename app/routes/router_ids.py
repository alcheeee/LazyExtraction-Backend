from ..database.UserCRUD import user_crud
from ..services.job_service import job_service

class RouteIDs:
    def __init__(self, route_name_id, user):
        self.route_name_id = route_name_id
        self.user = user

    def find_id(self):

        actions = {
            "play-game-button": lambda: user_crud.adjust_energy(self.user.id, -5),
            "quit-job": lambda: job_service.update_user_job(self.user.id, 'quit'),
            "work-job-button": lambda: job_service.do_user_job(self.user.id, self.user.job),
            "store-bagger-job": lambda: job_service.update_user_job(self.user.id, 'Store Bagger'),
        }

        if self.route_name_id in actions:
            results, msg = actions[self.route_name_id]()
            return results, msg
        else:
            return None, "Unknown action"