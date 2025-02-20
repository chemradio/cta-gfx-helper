from enum import Enum


class OrderRequestType(str, Enum):
    VIDEO_AUTO = "video_auto"
    VIDEO_FILES = "video_files"
    VIDEO_MIXED = "video_mixed"
    ONLY_SCREENSHOTS = "only_screenshots"
    READTIME = "readtime"
