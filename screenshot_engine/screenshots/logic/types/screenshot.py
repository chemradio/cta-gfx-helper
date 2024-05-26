from dataclasses import dataclass
from io import BytesIO
from shared.orders.order_base import OrderBase
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


@dataclass
class ScreenshotResults(OrderBase):
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

