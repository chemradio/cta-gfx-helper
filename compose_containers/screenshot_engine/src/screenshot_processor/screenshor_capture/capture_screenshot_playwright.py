"""Playwright counterpart of ``capture_screenshot.capture_crop_single_screenshot``.

The actual pixel grab is byte-for-byte the same CDP call the Selenium backend
used (``Page.captureScreenshot`` with ``captureBeyondViewport: False``) - only
the transport differs: a Playwright CDP session instead of Selenium's private
``command_executor._request``. The resulting ``Screenshot`` is cropped by the
shared, unchanged ``crop_screenshot``.
"""

import base64
import json
import os
from io import BytesIO

from playwright.sync_api import CDPSession, ElementHandle, Page

from py_gfxhelper_lib.custom_types import (
    Screenshot,
    ScreenshotRole,
    PostCoordinates,
    PostDimensions,
)
from .crop_screenshot import crop_screenshot


def capture_crop_single_screenshot(
    page: Page,
    cdp_session: CDPSession,
    target_element: ElementHandle,
    role: ScreenshotRole = ScreenshotRole.FULL_SIZE,
    dpi_multiplier: int | float = 2,
) -> Screenshot:
    """Capture the viewport via CDP, then crop to ``target_element``.

    ``target_element`` coordinates come from ``bounding_box()`` (CSS pixels,
    viewport-relative). The page routines scroll to the top before returning an
    element, so viewport-relative == document-relative here - exactly the
    assumption the Selenium ``.location`` path relied on."""
    # optional font smoothing - ON by default
    if os.environ.get("FONT_SMOOTHING", True):
        page.evaluate(
            'document.querySelector("body").style.textShadow = "0px 0px 1px rgba(0,0,0,.7)"'
        )

    box = target_element.bounding_box() or {"x": 0, "y": 0, "width": 0, "height": 0}
    element_coordinates = PostCoordinates(x=box["x"], y=box["y"])
    element_dimensions = PostDimensions(width=box["width"], height=box["height"])

    chrome_screenshot = cdp_session.send(
        "Page.captureScreenshot",
        {
            "format": "png",
            "captureBeyondViewport": False,
        },
    )

    content = BytesIO(base64.b64decode(chrome_screenshot["data"]))
    screenshot = Screenshot(
        content=content,
        role=role,
        element_dimensions=element_dimensions,
        element_coordinates=element_coordinates,
        cropped=False,
    )
    return crop_screenshot(screenshot, dpi_multiplier)
