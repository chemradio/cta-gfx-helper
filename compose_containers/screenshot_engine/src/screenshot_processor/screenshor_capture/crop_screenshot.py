from io import BytesIO

from PIL import Image

from py_gfxhelper_lib.custom_types import Screenshot, ScreenshotRole

Image.MAX_IMAGE_PIXELS = 933_120_000


def crop_screenshot(screenshot: Screenshot, dpi_multiplier: int | float) -> Screenshot:
    im = Image.open(screenshot.content)

    if screenshot.role == ScreenshotRole.POST:
        # must multiply by zoom or dpi multiplier
        left = screenshot.element_coordinates.x * dpi_multiplier
        top = screenshot.element_coordinates.y * dpi_multiplier
        right = (
            screenshot.element_coordinates.x + screenshot.element_dimensions.width
        ) * dpi_multiplier
        bottom = (
            screenshot.element_coordinates.y + screenshot.element_dimensions.height
        ) * dpi_multiplier

        # first crop
        im = im.crop((left, top, right, bottom))

        # clamp height to 5000px
        im = im.crop((0, 0, im.width, min(5000, im.height)))

    elif screenshot.role == ScreenshotRole.FULL_SIZE:
        im = im.crop((0, 0, im.width, min(7000, im.height)))

    cropped_content = BytesIO()
    im.save(cropped_content, format="PNG")

    screenshot.content = cropped_content
    return screenshot
