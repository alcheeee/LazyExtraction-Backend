import logging

class ExcludeMessageFilter(logging.Filter):
    def filter(self, record):
        return "error reading bcrypt version" not in record.getMessage()


def setup_logging():
    if not logging.root.handlers:
        logging.basicConfig(filename='app/logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        exclude_filter = ExcludeMessageFilter()
        for handler in logging.root.handlers:
            handler.addFilter(exclude_filter)