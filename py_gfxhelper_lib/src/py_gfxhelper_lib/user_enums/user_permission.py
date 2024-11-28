from enum import Enum


class UserPermission(str, Enum):
    UNREGISTERED: str = "UNREGISTERED"
    APPROVED: str = "APPROVED"
    BLOCKED: str = "BLOCKED"
    PENDING: str = "PENDING"
    ADMIN: str = "ADMIN"
