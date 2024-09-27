from typing import Optional, Dict, Any, Generic, TypeVar
from pydantic import BaseModel
from app.globals import DataName


class FailedResponse(BaseModel):
    detail: Optional[str] = "Error Message"


error_responses = {
    400: {"model": FailedResponse, "description": "Mechanics Error (e.g. not enough quantity)"},
    403: {"model": FailedResponse, "description": "Access Forbidden (Not Authenticated, if applicable)"},
    404: {"model": FailedResponse, "description": "Not Found (e.g. item not found)"},
    500: {"model": FailedResponse, "description": "Internal Server Error"}
}
