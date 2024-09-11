import traceback
from functools import wraps
from fastapi import Depends, Request
from .logger import MyLogger
from .HTTP_errors import CommonHTTPErrors


error_log = MyLogger.errors()


async def handle_exception(e, kwargs, log_type):
    """ Helper function to handle exception logging and raising proper HTTP errors. """
    session = kwargs.get('session', None)
    if session:
        await session.rollback()

    user_id = None
    if 'user_data' in kwargs:
        user_data = kwargs.get('user_data')
        if user_data and 'user' in user_data:
            user_id = user_data['user']['user_id']

    request = kwargs.get('request', None)

    # Extract function name where exception occurred
    tb = traceback.extract_tb(e.__traceback__)
    function_name = tb[-1].name

    if log_type != 'mechanics_error':
        # Log the exception if not intentional
        MyLogger.log_exception(
            logger=error_log,
            e=e,
            user_id=user_id,
            input_data=request,
            function_name=function_name
        )

    # Raise HTTP error based exception type
    if log_type == 'mechanics_error':
        raise CommonHTTPErrors.mechanics_error(str(e))
    elif log_type == 'index_error':
        raise CommonHTTPErrors.index_error(str(e))
    else:
        raise CommonHTTPErrors.server_error()


def exception_decorator(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except ValueError as e:
            await handle_exception(e, kwargs, log_type='mechanics_error')

        except LookupError as e:
            await handle_exception(e, kwargs, log_type='index_error')

        except Exception as e:
            await handle_exception(e, kwargs, log_type='server_error')

    return decorator
