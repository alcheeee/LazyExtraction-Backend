from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(0.3, 1.5)
    # 200 Users
    # 50 Ramp up
    # 30s Run time

    @task
    def create_item_old(self):
        self.client.post("/admin/create-item/equippable",
                         json={
                          "item_name": "Bandana",
                          "quantity": 10,
                          "illegal": False,
                          "category": "Clothing",
                          "randomize_all": True,
                          "randomize_stats": False,
                          "quick_sell": 0,
                          "quality": "Junk",
                          "clothing_type": "Mask",
                          "reputation_bonus": 0,
                          "max_energy_bonus": 0,
                          "damage_bonus": 0,
                          "evasiveness_bonus": 0,
                          "health_bonus": 0,
                          "luck_bonus": 0,
                          "strength_bonus": 0,
                          "knowledge_bonus": 0
                        })