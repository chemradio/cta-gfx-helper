import time

SLEEP_DELAY_1S = 2


def sleep_before_after(function, sleep_time: int = SLEEP_DELAY_1S):
    def wrapper(*args, **kwargs):
        time.sleep(sleep_time)
        value = function(*args, **kwargs)
        time.sleep(sleep_time)
        return value

    return wrapper
