from enum import Enum


class DataName(str, Enum):
    NewUser = "created-user"
    RoomData = "room-data"
    UserStats = "user-stats"
    UserInventory = "user-inventory"
    AllInventoryItems = "all-inventory-items"
    InventoryItem = "inventory-item"
    WeaponData = "weapon-data"
