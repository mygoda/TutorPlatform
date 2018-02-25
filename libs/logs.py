import logging


def log_message(message, **kwargs):
    return "[%s]" % message


class InfoLevelFilter(logging.Filter):
    def filter(self, record):
        if record.levelname == "INFO":
            return 1
        else:
            return 0


class WarningLevelFilter(logging.Filter):
    def filter(self, record):
        if record.levelname == "WARNING":
            return 1
        else:
            return 0