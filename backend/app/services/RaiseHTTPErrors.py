from fastapi import HTTPException, status
from ..utils.logger import MyLogger

class CommonHTTPErrors:
    def __init__(self):
        self.admin_log = MyLogger.admin()

    @staticmethod
    def credentials_error():
        """Raise an HTTP 401 error indicating credential validation failure"""
        error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return error

    @staticmethod
    def mechanics_error(message: str):
        """Raises an HTTP 400 error with a custom message"""
        error = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
        return error

    @staticmethod
    def server_error(message="Internal Server Error"):
        """Raises an HTTP 500 server error"""
        error = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
        return error


raise_http_error = CommonHTTPErrors()
