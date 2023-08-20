from dataclasses import dataclass


@dataclass
class PostDimensions:
    width: int
    height: int


@dataclass
class PostCoordinates:
    x: int
    y: int
