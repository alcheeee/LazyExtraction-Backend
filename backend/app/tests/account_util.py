from typing import Optional, Dict, List


class UserAccount:
    def __init__(self, username="test-user"):
        self.username: str = f"{username}"
        self.email: str = f"{self.username}@test.com"
        self.password: str = f"123456"
        self.auth_token: Optional[str] = None
        self.headers: Dict[str, str] = {"Authorization": ""}
        self.raid = UserAccount.UserRaid()
        self.inventory = UserAccount.Inventory()

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
            room_data = json_data.get('room-data', {})
            if room_data:
                self.room_data = room_data
                self.items = room_data.get('items', [])
                self.connections = room_data.get('connections', [])

        def pop_raid_item_id(self) -> Optional[int]:
            if not self.items:
                return None
            item_id = self.items.pop(0)["id"]
            self.interaction_count += 1
            return item_id

        def pop_connection(self) -> Optional[int]:
            if not self.connections:
                return None
            self.interaction_count += 1
            return self.connections.pop(0)

    class Inventory:
        def __init__(self):
            self.inventory_data: dict = {}

        def item_picked_up(self, item_name: str):
            if item_name not in self.inventory_data:
                self.inventory_data[item_name] = 1
                return
            self.inventory_data[item_name] += 1


