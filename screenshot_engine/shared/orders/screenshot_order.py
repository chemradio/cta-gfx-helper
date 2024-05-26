from shared.orders.order_base import OrderBase
from typing import Any
from dataclasses import field
from shared.utils.generate_filename import generate_filename, FilenameType
import pydantic


class ScreenshotOrderIn(pydantic.BaseModel):
    screenshot_link: pydantic.networks.AnyHttpUrl
    secret_key: str | None = None


class ScreenshotOrder(OrderBase):
    def __init__(self, screenshot_link: str):
        super().__init__()
        self.screenshot_link = screenshot_link

    screenshot_link: str
    results: Any = None

    # output
    bg_filename: str = field(
        default_factory=lambda: generate_filename(FilenameType.SCREENSHOT_BACKGROUND)
    )
    fg_filename: str = field(
        default_factory=lambda: generate_filename(FilenameType.SCREENSHOT_FOREGROUND)
    )

    def to_dict(self):
        return {
            "screenshot_link": self.screenshot_link,
            "bg_filename": self.bg_filename,
            "fg_filename": self.fg_filename,
            "results": "ScreenshotResults obj placeholder",
        }.update(super().to_dict())
