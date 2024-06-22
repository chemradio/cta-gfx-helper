from io import BytesIO

from PIL import Image

from .types import Screenshot, ScreenshotRole

Image.MAX_IMAGE_PIXELS = 933_120_000


def crop_screenshot(screenshot: Screenshot, dpi_multiplier: int | float) -> Screenshot:
    im = Image.open(screenshot.content)

    if screenshot.role == ScreenshotRole.POST:
        # must multiply by zoom or dpi multiplier
        left = screenshot.post_coordinates.x * dpi_multiplier
        top = screenshot.post_coordinates.y * dpi_multiplier
        right = (
            screenshot.post_coordinates.x + screenshot.post_dimensions.width
        ) * dpi_multiplier
        bottom = (
            screenshot.post_coordinates.y + screenshot.post_dimensions.height
        ) * dpi_multiplier

        im = im.crop((left, top, right, bottom))
        im = im.crop((0, 0, im.width, min(5000, im.height)))

    elif screenshot.role == ScreenshotRole.FULL_SIZE:
        im = im.crop((0, 0, im.width, min(7000, im.height)))

    cropped_content = BytesIO()
    im.save(cropped_content, format="PNG")

    screenshot.content = cropped_content
    return screenshot
