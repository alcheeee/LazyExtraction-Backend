from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(0.3, 1.5)
    # 200 Users
    # 50 Ramp up
    # 30s Run time

    @task
    def create_item_old(self):
        self.client.post("/game/job-action",
                         json={
                            "job_action": "apply",
                            "job_name": "Cook"
                         }
                    )

