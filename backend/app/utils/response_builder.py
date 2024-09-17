from typing import Union, Any
from enum import Enum
from .HTTP_errors import CommonHTTPErrors


class DataName(str, Enum):
    RoomData = "room-data"
    UserStats = "user-stats"
    UserInventory = "user-inventory"
    AllInventoryItems = "all-inventory-items"
    InventoryItem = "inventory-item"
    WeaponData = "weapon-data"


class ResponseBuilder:

    @staticmethod
    def success(message: str, data_name: DataName = None, data: Union[dict, Any] = {}) -> dict:
        response = {"status": "success", "message": message}
        if data or data_name:
            data_name = "data" if data_name is None else data_name.value
            response[data_name] = data
        return response
