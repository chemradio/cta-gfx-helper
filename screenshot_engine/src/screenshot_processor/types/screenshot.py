from dataclasses import dataclass
from io import BytesIO

from .post_location_size import PostCoordinates, PostDimensions
from .screenshot_role import ScreenshotRole


@dataclass
class Screenshot:
    content: BytesIO
    role: ScreenshotRole
    element_dimensions: PostDimensions | None = None
    element_coordinates: PostCoordinates | None = None
    cropped: bool = False