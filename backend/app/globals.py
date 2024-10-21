from enum import Enum


class PotentialAPIAccess(Exception):
    """ Raised when errors occur that shouldn't be raised, unless directly through the API """
    # TODO : Add this exception
    pass


class DataName(str, Enum):
    UserData = "user-data"
    RoomData = "room-data"
    UserStats = "user-stats"
    UserInventory = "user-inventory"
    AllInventoryItems = "all-inventory-items"
    InventoryItem = "inventory-item"
    WeaponData = "updated-weapon-data"
