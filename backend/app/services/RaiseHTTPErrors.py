from fastapi import HTTPException, status
from ..utils.logger import MyLogger

class CommonHTTPErrors:
    def __init__(self):
        self.admin_log = MyLogger.admin()

    def raise_credentials_error(self):
        """Raise an HTTP 401 error indicating credential validation failure"""
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def raise_mechanics_error(self, message: str):
        """Raises an HTTP 400 error with a custom message"""
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    def raise_server_error(self):
        """Raises an HTTP 500 server error"""
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


raise_http_error = CommonHTTPErrors()
