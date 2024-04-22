import random
import string
from enum import Enum
from datetime import datetime

class ScreenshotFilenameType(Enum):
    BACKGROUND = "1_BG"
    FOREGROUND = "2_FG"


def generate_filename(
    type: ScreenshotFilenameType = ScreenshotFilenameType.BACKGROUND,
) -> str:
    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=16))

    # generate time in HH:MM:SS format
    time = datetime.now().strftime("%H_%M_%S")


    return f"{type.value}_{time}_{random_string}.png"


