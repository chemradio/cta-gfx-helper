from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    NORMAL = "NORMAL"


class NormalUserPermission(str, Enum):
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"


class SystemEventType(str, Enum):
    WARNING = "WARNING"
    ERROR = "ERROR"


class OrderRequestType(str, Enum):
    VIDEO_AUTO = "video_auto"
    VIDEO_FILES = "video_files"
    ONLY_SCREENSHOTS = "only_screenshots"
    READTIME = "readtime"


class OrderSource(str, Enum):
    WEB = "web"
    TELEGRAM = "telegram"
