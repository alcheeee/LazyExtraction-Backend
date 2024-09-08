from enum import Enum
from .HTTP_errors import common_http_errors


class DataName(str, Enum):
    ItemDetails = "item-details"
    ItemGiven = "item-given"
    RoomData = "room-data"
    UserStats = "user-stats"
    UserInventory = "user-inventory"
    InventoryItem = "inventory-item"


class ResponseBuilder:

    @staticmethod
    def success(message: str, data_name: DataName = None, data: dict = None) -> dict:
        response = {"status": "success", "message": message}
        if data:
            response[data_name.value] = data
        return response
