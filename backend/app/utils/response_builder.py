from enum import Enum


class DataName(str, Enum):
    ItemDetails = "item-details"
    ItemGiven = "item-given"


class ResponseBuilder:

    @staticmethod
    def success(message: str, data_name: DataName = None, data: dict = None) -> dict:
        response = {"status": "success", "message": message}
        if data:
            response[data_name.value] = data
        return response


    @staticmethod
    def error(message: str, error_code: int = 400) -> dict:
        return {"status": "error", "message": message, "error_code": error_code}
