import base64
import json
import os
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from ..types import PostCoordinates, PostDimensions, Screenshot, ScreenshotRole


def capture_single_screenshot(
    driver: webdriver.Remote,
    target_element: WebElement,
    role: ScreenshotRole = ScreenshotRole.FULL_SIZE,
) -> Screenshot:
    # optional font smoothing - ON by default
    if os.environ.get("FONT_SMOOTHING", True):
        driver.execute_script(
            'document.querySelector("body").style.textShadow = "0px 0px 1px rgba(0,0,0,.7)"'
        )

    element_coordinates = PostCoordinates(
        x=target_element.location["x"],
        y=target_element.location["y"],
    )

    element_dimensions = PostDimensions(
        width=target_element.size["width"],
        height=target_element.size["height"],
    )

    chrome_screenshot = driver.command_executor._request(
        "POST",
        driver.command_executor._url
        + f"/session/{driver.session_id}/chromium/send_command_and_get_result",
        json.dumps(
            {
                "cmd": "Page.captureScreenshot",
                "params": {
                    "format": "png",
                    "captureBeyondViewport": False,
                },
            }
        ),
    )

    content = BytesIO(base64.urlsafe_b64decode(chrome_screenshot["value"]["data"]))
    return Screenshot(
        content=content,
        role=role,
        element_dimensions=element_dimensions,
        element_coordinates=element_coordinates,
        cropped=False,
    )
