from enum import Enum


class OrderRequestType(str, Enum):
    VIDEO_AUTO = "video_auto"
    VIDEO_FILES = "video_files"
    VIDEO_MIXED = "video_mixed"
    ONLY_SCREENSHOTS = "only_screenshots"
    READTIME = "readtime"


class OrderStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    ERROR_TERMINATED = "error_terminated"
    ADMIN_TERMINATED = "admin_terminated"
    ORDER_CREATION = "order_creation"


class OrderSource(str, Enum):
    WEB = "web"
    TELEGRAM = "telegram"
