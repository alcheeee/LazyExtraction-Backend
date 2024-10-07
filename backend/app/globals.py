from enum import Enum


class DataName(str, Enum):
    UserData = "user-data"
    RoomData = "room-data"
    UserStats = "user-stats"
    UserInventory = "user-inventory"
    AllInventoryItems = "all-inventory-items"
    InventoryItem = "inventory-item"
    WeaponData = "updated-weapon-data"
