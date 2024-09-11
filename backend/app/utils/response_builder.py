from enum import Enum
from .HTTP_errors import CommonHTTPErrors


class DataName(str, Enum):
    ItemDetails = "item-details"
    ItemGiven = "item-given"
    RoomData = "room-data"
    UserStats = "user-stats"
    UserInventory = "user-inventory"
    InventoryItem = "inventory-items"


class ResponseBuilder:

    @staticmethod
    def success(message: str, data_name: DataName = None, data: dict = {}) -> dict:
        response = {"status": "success", "message": message}
        if data or data_name:
            data_name = "data" if data_name is None else data_name.value
            response[data_name] = data
        return response
