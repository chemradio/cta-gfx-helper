from enum import Enum


class DomainName(str, Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    TELEGRAM = "telegram"
    VK = "vk"
    OTHER = "other"
