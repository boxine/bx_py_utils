import logging


class RaiseLogUsage(logging.Handler):
    """
    A log handler, that raise an error on every log output.
    This is useful to check if tests generates not captured log output.
    """

    def handle(self, record):
        raise AssertionError(f'Missing log capture for: "{self.format(record)}"')
