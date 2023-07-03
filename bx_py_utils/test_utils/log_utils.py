import logging


class RaiseLogUsage(logging.Handler):
    """
    A log handler, that raise an error on every log output.
    This is useful to check if tests generates not captured log output.
    """

    def handle(self, record):
        raise AssertionError(f'Missing log capture for: "{self.format(record)}"')


class NoLogs:
    """
    Context manager to Suppress all logger outputs
    """

    def __init__(self, logger_name: str):
        self.logger_name = logger_name

    def __enter__(self):
        self.logger = logging.getLogger(self.logger_name)
        self.origin_handlers = self.logger.handlers
        self.logger.handlers = [logging.NullHandler()]

    def __exit__(self, exc_type, exc_value, tb):
        self.logger.handlers = self.origin_handlers
        if exc_type:
            # let unexpected exceptions pass through
            return False
