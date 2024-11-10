from enum import Enum


class SystemEventType(str, Enum):
    WARNING = "WARNING"
    ERROR = "ERROR"
