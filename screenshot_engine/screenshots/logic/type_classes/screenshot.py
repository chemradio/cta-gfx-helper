from dataclasses import dataclass, field
from io import BytesIO

from screenshots.logic.type_classes.post_location_size import (
    PostCoordinates,
    PostDimensions,
)
from screenshots.logic.type_classes.screenshot_role import ScreenshotRole
from utils.generate_filename import generate_filename, ScreenshotFilenameType

from utils.generate_order_id import generate_order_id


@dataclass
class Screenshot:
    content: BytesIO
    role: ScreenshotRole
    post_dimensions: PostDimensions | None = None
    post_coordinates: PostCoordinates | None = None
    cropped: bool = False


@dataclass
class ScreenshotResults:
    success: bool = False
    background: Screenshot | None = None
    foreground: Screenshot | None = None
    two_layer: bool = False
    error_message: str | None = None

    def to_dict(self):
        return {
            "success": self.success,
            "background": "BytesIO object placeholder",
            "foreground": "BytesIO object placeholder",
            "two_layer": self.two_layer,
            "error_message": self.error_message,
        }


@dataclass
class ScreenshotOrder:
    screenshot_link: str
    order_id: str = field(default_factory=generate_order_id)
    bg_filename: str = field(
        default_factory=lambda: generate_filename(ScreenshotFilenameType.BACKGROUND)
    )
    fg_filename: str = field(
        default_factory=lambda: generate_filename(ScreenshotFilenameType.FOREGROUND)
    )
    results: ScreenshotResults = field(default_factory=ScreenshotResults)

    def to_dict(self):
        return {
            "screenshot_link": self.screenshot_link,
            "order_id": self.order_id,
            "bg_filename": self.bg_filename,
            "fg_filename": self.fg_filename,
            "results": self.results.to_dict(),
        }
