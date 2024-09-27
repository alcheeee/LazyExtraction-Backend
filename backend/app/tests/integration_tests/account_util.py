from typing import Optional, Dict, List


class UserAccount:
    def __init__(self, username="test-user"):
        self.username: str = f"{username}"
        self.email: str = f"{self.username}@test.com"
        self.password: str = f"test-user"
        self.auth_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.headers: Dict[str, str] = {"Authorization": ""}
        self.raid = UserAccount.UserRaid()
        self.inventory = UserAccount.Inventory()
        self.posted_items = []

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
            self.main_inventory_data: dict = {}
            self.inventory_data: dict = {}
            self.equipped_items: dict = {}
            self.last_unequipped_item: dict = None
            self.admin_provided_item: dict = {}
            self.temp_data: dict

        def item_picked_up(self, item_data: dict):
            inv_item = item_data['inv_item']
            item_id = str(inv_item['item_id'])

            if item_id not in self.inventory_data:
                self.inventory_data[item_id] = inv_item
            else:
                self.inventory_data[item_id]['amount_in_inventory'] += 1

        def get_an_item(self):
            item_id = next(iter(self.inventory_data))
            return self.inventory_data[item_id]

        def equip_item(self, item_data: dict):
            self.equipped_items[item_data['id']] = item_data

        def unequip_item(self, item_data: dict):
            self.equipped_items.pop(item_data['id'], None)
            self.last_unequipped_item = item_data

        def get_equipped_item(self):
            return next(iter(self.equipped_items.values())) if self.equipped_items else None

        def get_last_unequipped_item(self):
            return self.last_unequipped_item

        def get_admin_provided_item(self):
            return next(iter(self.admin_provided_item.values())) if self.admin_provided_item else None
