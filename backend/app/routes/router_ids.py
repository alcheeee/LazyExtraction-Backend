from ..game_systems.jobs.JobHandler import JobService

class RouteIDs:
    def __init__(self, route_name_id, user_id, session):
        self.route_name_id = route_name_id
        self.user_id = user_id
        self.session = session

    async def find_id(self):
        actions = {
            #"work-job": lambda: job_service.do_user_job(self.user, self.user.stats.job, session=self.session),
            #"quit-job": lambda: job_service.update_user_job(self.user, 'quit', session=self.session),
        }
        try:
            if self.route_name_id in actions:
                    msg = await actions[self.route_name_id]()
                    return {"message": msg}
            else:
                raise ValueError("Not a valid button")

        except ValueError as e:
            raise e
        except Exception as e:
            raise e
