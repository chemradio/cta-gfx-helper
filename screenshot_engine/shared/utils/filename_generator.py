import random
import string
from enum import Enum
from datetime import datetime

class FilenameType(Enum):
    SCREENSHOT_BACKGROUND = "1_BG_{}.png"
    SCREENSHOT_FOREGROUND = "2_FG_{}.png"
    VIDEOGFX_VIDEO = "VideoGFX_{}.mp4"


def generate_filename(
    type: FilenameType,
) -> str:
    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=16))
    time = datetime.now().strftime("%H_%M_%S")
    return type.value.format(f"{time}_{random_string}")

