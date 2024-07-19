from typing import Optional, Dict, List


class UserAccount:
    def __init__(self, username="test-user"):
        self.username: str = f"{username}"
        self.email: str = f"{self.username}@test.com"
        self.password: str = f"123456"
        self.auth_token: Optional[str] = None
        self.headers: Dict[str, str] = {"Authorization": ""}
        self.raid = UserAccount.UserRaid()

    def set_auth_token(self, token: str):
        self.auth_token = token
        self.headers["Authorization"] = f"Bearer {self.auth_token}"


    class UserRaid:
        def __init__(self):
            self.in_raid: bool = False
            self.interaction_count: int = 0
            self.room_data: Optional[Dict] = None
            self.items: Optional[List[Dict]] = None
            self.connections: Optional[List] = None

        def set_in_raid(self, raid_status: bool, json_data: Optional[Dict] = None):
            self.in_raid = raid_status
            room_data = json_data['room-data']
            if room_data:
                self.room_data = room_data
                self.items = room_data['items']
                self.connections = room_data['connections']

        def add_interaction(self):
            self.interaction_count += 1

        def pop_raid_item_id(self) -> Optional[int]:
            self.add_interaction()
            return self.items.pop()["id"]

        def pop_connection(self) -> Optional[int]:
            return self.connections.pop()
