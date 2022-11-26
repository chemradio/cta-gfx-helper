import re
from time import strftime, gmtime
from config import Readspeed


def calc_readtime(text, wpm: Readspeed = Readspeed.MEDIUM.value):
    words = re.findall(r"[а-яА-Яa-zA-Z]+", text)
    digits = re.findall(r"[1-9]", text)
    word_count = len(words) + len(digits)
    seconds = word_count / wpm * 60
    readtime = strftime("%M мин. %S сек.", gmtime(seconds))
    return readtime
