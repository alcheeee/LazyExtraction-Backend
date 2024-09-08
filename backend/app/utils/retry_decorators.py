from functools import wraps
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError
)
from sqlalchemy.exc import (
    DBAPIError,
    OperationalError,
    InternalError
)
from .logger import MyLogger


db_log = MyLogger.database()
error_log = MyLogger.errors()


class RetryDecorators:
    @staticmethod
    def db_retry_decorator(max_attempts=3, wait_min=1, wait_max=10):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                retryer = retry(
                    stop=stop_after_attempt(max_attempts),
                    wait=wait_exponential(multiplier=1, min=wait_min, max=wait_max),
                    retry=(
                            retry_if_exception_type(DBAPIError) |
                            retry_if_exception_type(OperationalError) |
                            retry_if_exception_type(InternalError)
                    ),
                    before_sleep=lambda retry_state: db_log.warning(
                        f"Retrying {func.__name__} due to {retry_state.outcome.exception()}. "
                        f"Attempt {retry_state.attempt_number} of {max_attempts}"
                    ),
                    reraise=True
                )
                try:
                    return await retryer(func)(*args, **kwargs)
                except RetryError as e:
                    db_log.error(f"All retry attempts failed for {func.__name__}: {str(e)}")
                    raise
            return wrapper
        return decorator
