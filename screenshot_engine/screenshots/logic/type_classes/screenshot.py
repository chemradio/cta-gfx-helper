from dataclasses import dataclass
from io import BytesIO

from screenshots.logic.type_classes.post_location_size import (
    PostCoordinates,
    PostDimensions,
)
from screenshots.logic.type_classes.screenshot_role import ScreenshotRole


@dataclass
class Screenshot:
    content: BytesIO
    role: ScreenshotRole
    post_dimensions: PostDimensions | None = None
    post_coordinates: PostCoordinates | None = None
    cropped: bool = False
    filename: str | None = None


@dataclass
class ScreenshotResults:
    success: bool = True
    background: Screenshot | None = None
    foreground: Screenshot | None = None
    two_layer: bool = False
