from dataclasses import dataclass

from helpers.enums.enum_selenium_image import SeleniumImage


@dataclass
class DefaultContainerImages:
    db = "postgres:15-alpine"
    screenshot_selenium = SeleniumImage.NORMAL
    video_gfx_selenium = SeleniumImage.NORMAL
