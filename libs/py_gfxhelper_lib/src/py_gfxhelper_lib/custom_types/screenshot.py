from dataclasses import dataclass
from io import BytesIO
from enum import Enum, auto


class ScreenshotRole(Enum):
    POST = auto()
    FULL_SIZE = auto()


@dataclass
class PostDimensions:
    width: int
    height: int


@dataclass
class PostCoordinates:
    x: int
    y: int


@dataclass
class Screenshot:
    content: BytesIO
    role: ScreenshotRole = ScreenshotRole.FULL_SIZE
    element_dimensions: PostDimensions | None = None
    element_coordinates: PostCoordinates | None = None
    cropped: bool = False
