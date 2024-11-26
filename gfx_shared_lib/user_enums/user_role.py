from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    NORMAL = "NORMAL"
