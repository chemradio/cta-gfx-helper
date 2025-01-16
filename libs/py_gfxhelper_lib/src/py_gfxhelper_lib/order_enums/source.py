from enum import Enum


class OrderSource(str, Enum):
    WEB = "web"
    TELEGRAM = "telegram"
