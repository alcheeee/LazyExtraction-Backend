from fastapi import HTTPException, status
from .logger import MyLogger


user_log = MyLogger.user()


class CommonHTTPErrors:

    @staticmethod
    def credentials_error(
            message="Could not validate credentials",
            exception: str = "Credential Error",
            data: dict = None
    ):
        """Raise an HTTP 401 error indicating credential validation failure"""
        error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )
        user_id = None
        if data and data.get('user'):
            data = data['user']
            user_id = data.get('user_id', None)

        MyLogger.log_exception(user_log, str(exception), input_data=data)
        return error



    @staticmethod
    def mechanics_error(message: str = "Error"):
        """Raises an HTTP 400 error with a custom message"""
        error = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
        return error

    @staticmethod
    def server_error(message: str = "Internal Server Error"):
        """Raises an HTTP 500 server error"""
        error = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
        return error

    @staticmethod
    def index_error(message: str = "Unable to index"):
        """Raises an HTTP 404 error"""
        error = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )
        return error
