from ..database.UserCRUD import user_crud
from ..game_systems.Jobs.AccessAllJobs import update_user_job, work_users_job
from ..database.GameplayCRUDS.CorporationCRUD import corporation_manager

class RouteIDs:
    def __init__(self, route_name_id, user):
        self.route_name_id = route_name_id
        self.user = user

    def find_id(self):

        actions = {
            "play-game-button": lambda: user_crud.adjust_energy(self.user.id, -5),
            "work-job-button": lambda: work_users_job(self.user.id),
            "store-bagger-job": lambda: update_user_job(self.user.id, 'Store Bagger'),
        }

        if self.route_name_id in actions:
            results, msg = actions[self.route_name_id]()
            return results, msg
        else:
            return None, "Unknown action"

