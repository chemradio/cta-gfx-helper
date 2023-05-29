from enum import Enum


class UploadFileCategory(str, Enum):
    SCREENSHOTS = "screenshots"
    VIDEO_EXPORTS = "video_exports"
    USER_FILES = "user_files"
