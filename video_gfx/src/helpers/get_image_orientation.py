from PIL import Image

from src.types import ImageOrientation


def get_image_orientation(image_path: str) -> ImageOrientation:
    with Image.open(image_path, "r") as im:
        ratio = im.width / im.height
        if ratio < 0.8:
            return ImageOrientation.VERTICAL
        else:
            return ImageOrientation.HORIZONTAL
