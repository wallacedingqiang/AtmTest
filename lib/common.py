import logging.config
from conf import settings


def auth_register(func):
    from core import src

    def inner(*args, **kwargs):
        if src.user_info:
            res = func(*args, **kwargs)
            return res
        else:
            src.login()

    return inner


def get_logger(name):
    logging.config.dictConfig(settings.LOGGING_DIC)

    logger = logging.getLogger(name)

    return logger
