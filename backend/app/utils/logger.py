import os
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

        log_dir = 'app/logs/'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        exclude_filter = ExcludeMessageFilter()
        logs = {
            'errors': 'app/logs/error_logs.log',
            'auth_errors': 'app/logs/auth_error_logs.log',
            'game': 'app/logs/game_logs.log',
            'admin': 'app/logs/admin_logs.log',
            'user': 'app/logs/user_logs.log',
            'database': 'app/logs/db_logs.log',
        }
        for name, path in logs.items():
            handler = RotatingFileHandler(path, maxBytes=10000000, backupCount=5)
            handler.setLevel(logging.INFO)
            handler.setFormatter(log_formatter)
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
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
    def auth_errors():
        return MyLogger.get_logger('auth_errors')
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
    def log_exception(logger, e=None, user_id=None, input_data=None, function_name=None):
        user_id_text = f"--> User id: {user_id}\n" if user_id else ""
        error_message = (
            f"Unexpected error in {function_name}: {str(e)}\n"
            f"{user_id_text}--> Input: {input_data}\n"
        )
        logger.error(error_message)






