from functools import wraps
from fastapi import Depends, Request
from .logger import MyLogger
from .HTTP_errors import common_http_errors


error_log = MyLogger.errors()


def exception_decorator(func):
    @wraps(func)
    async def decorator(request: Request, *args, **kwargs):
        try:
            return await func(request, *args, **kwargs)

        except ValueError as e:
            if 'session' in kwargs:
                await kwargs['session'].rollback()
            print(str(e))
            raise common_http_errors.mechanics_error(str(e))

        except Exception as e:
            if 'session' in kwargs:
                await kwargs['session'].rollback()

            # Check if user_id is a route dependency
            user_id = None
            for name, value in func.__annotations__.items():
                if name == 'user_id' and isinstance(value, Depends):
                    user_id = kwargs.get('user_id')
                    break

            requested_info = kwargs.get('request', None)

            MyLogger.log_exception(error_log, e, user_id, requested_info)
            raise common_http_errors.server_error()

    return decorator
