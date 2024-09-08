import inspect
import logging
from logging.handlers import RotatingFileHandler

class ExcludeMessageFilter(logging.Filter):
    def filter(self, record):
        return "error reading bcrypt version" not in record.getMessage()

class LogManager:
    _initialized = False
    @classmethod
    def setup_logging(cls):
        if cls._initialized:
            return

        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        exclude_filter = ExcludeMessageFilter()
        logs = {
            'errors': 'app/logs/error_logs.log',
            'game': 'app/logs/game_logs.log',
            'admin': 'app/logs/admin_logs.log',
            'user': 'app/logs/user_logs.log',
            'database': 'app/logs/db_logs.log',
        }
        for name, path in logs.items():
            handler = RotatingFileHandler(path, maxBytes=10000000, backupCount=5)
            handler.setLevel(logging.INFO)
            handler.setFormatter(log_formatter)
            handler.addFilter(exclude_filter)

            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)

        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            handler.addFilter(exclude_filter)
        cls._initialized = True

LogManager.setup_logging()

class MyLogger:
    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
    @staticmethod
    def errors():
        return MyLogger.get_logger('errors')
    @staticmethod
    def game():
        return MyLogger.get_logger('game')
    @staticmethod
    def admin():
        return MyLogger.get_logger('admin')
    @staticmethod
    def user():
        return MyLogger.get_logger('user')
    @staticmethod
    def database():
        return MyLogger.get_logger('database')

    @staticmethod
    def log_exception(logger, e, user_id, input_data):
        function_name = inspect.stack()[1].function
        error_message = (
            f"Unexpected error in {function_name}: {str(e)}\n"
            f"-> User id: {user_id} - Input: {input_data}"
        )
        logger.error(error_message)






