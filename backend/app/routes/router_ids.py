from ..services.job_service import job_service

class RouteIDs:
    def __init__(self, route_name_id, user, session):
        self.route_name_id = route_name_id
        self.user = user
        self.session = session

    async def find_id(self):
        actions = {
            "work-job": lambda: job_service.do_user_job(self.user, self.user.job, session=self.session),
            "quit-job": lambda: job_service.update_user_job(self.user, 'quit', session=self.session),
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
