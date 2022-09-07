import logging

logger_bot = logging.getLogger(__name__)
logger_bot.setLevel(logging.DEBUG)
logging_bot_formatter = logging.Formatter("%(asctime)s: %(name)s: %(message)s")
# logging_bot_file_handler = logging.FileHandler(f"./logs/{__name__}.log", mode='w+')
# logging_bot_file_handler.setLevel(logging.DEBUG)
# logging_bot_file_handler.setFormatter(logging_bot_formatter)
logging_bot_stream_handler = logging.StreamHandler()
logging_bot_stream_handler.setFormatter(logging_bot_formatter)
# logger_bot.addHandler(logging_bot_file_handler)
# logger_bot.addHandler(logging_bot_stream_handler)


def log_decorator(func):
    def wrapper(*args, **kwargs):
        logger_bot.debug(f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        logger_bot.debug(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper
