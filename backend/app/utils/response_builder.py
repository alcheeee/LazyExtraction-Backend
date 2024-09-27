from typing import Union, Any, Optional
from app.globals import DataName
from sqlmodel import SQLModel


class ResponseBuilder:

    @staticmethod
    def success(message: str, data_name: DataName = None, data: Union[dict, Any] = {}) -> dict:
        response = {"status": "success", "message": message}
        if data or data_name:
            data_name = "data" if data_name is None else data_name.value
            response[data_name] = data
        return response
