from functools import wraps
from fastapi import Depends, Request
from .logger import MyLogger
from .HTTP_errors import CommonHTTPErrors


error_log = MyLogger.errors()


def exception_decorator(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except ValueError as e:
            session = kwargs.get('session', None)
            if session:
                await session.rollback()
            raise CommonHTTPErrors.mechanics_error(str(e))

        except LookupError as e:
            session = kwargs.get('session', None)
            if session:
                await session.rollback()

            # Check if user_id is a route dependency
            user_id = None
            if 'user_data' in kwargs:
                user_data = kwargs.get('user_data')
                if user_data and 'user' in user_data:
                    user_id = user_data['user']['user_id']

            request = kwargs.get('request', None)

            MyLogger.log_exception(error_log, e, user_id, request)
            raise CommonHTTPErrors.index_error()

        except Exception as e:
            session = kwargs.get('session', None)
            if session:
                await session.rollback()

            # Check if user_id is a route dependency
            user_id = None
            if 'user_data' in kwargs:
                user_data = kwargs.get('user_data')
                if user_data and 'user' in user_data:
                    user_id = user_data['user']['user_id']

            request = kwargs.get('request', None)

            MyLogger.log_exception(error_log, e, user_id, request)
            raise CommonHTTPErrors.server_error()

    return decorator

