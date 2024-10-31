import random
import string
from datetime import datetime
from enum import Enum


class FilenameType(str, Enum):
    SCREENSHOT_BACKGROUND = "1_BG_{}.png"
    SCREENSHOT_FOREGROUND = "2_FG_{}.png"
    SCREENSHOT_IMAGE = "SCREENSHOT_{}.png"
    VIDEOGFX_VIDEO = "VideoGFX_{}.mp4"


def generate_filename(
    filename_type: FilenameType,
) -> str:
    random_string = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=16)
    )
    time = datetime.now().strftime("%H_%M_%S")
    return filename_type.value.format(f"{time}_{random_string}")
