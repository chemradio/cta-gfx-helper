from enum import Enum


class UserStatus(Enum):
    UNREGISTERED: str = "unregistered"
    ALLOWED: str = "allowed"
    BLOCKED: str = "blocked"
    PENDING: str = "pending"
    ADMIN: str = "admin"
