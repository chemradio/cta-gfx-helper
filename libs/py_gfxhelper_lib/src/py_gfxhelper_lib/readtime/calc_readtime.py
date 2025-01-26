import re
from time import strftime, gmtime
from .readspeed import Readspeed


def calc_readtime(text, readspeed: Readspeed = Readspeed.MEDIUM):
    words = re.findall(r"[а-яА-Яa-zA-Z]+", text)
    digits = re.findall(r"[1-9]", text)
    word_count = len(words) + len(digits)
    seconds = word_count / readspeed.value * 60
    readtime = (
        strftime("%M мин. %S сек.", gmtime(seconds))
        if seconds > 60
        else f"{round(int(seconds))} сек."
    )
    return readtime
