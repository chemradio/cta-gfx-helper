import base64
import json
import os
from io import BytesIO

from selenium import webdriver

from ..page_routines import post_workflow, profile_workflow
from ..types import PostCoordinates, PostDimensions, Screenshot, ScreenshotRole


def capture_single_screenshot(
    driver: webdriver.Remote,
    role: ScreenshotRole = ScreenshotRole.FULL_SIZE,
) -> Screenshot:
    if role == ScreenshotRole.POST:
        target_element = post_workflow(driver)
    elif role == ScreenshotRole.FULL_SIZE:
        target_element = profile_workflow(driver)

    # optional font smoothing - ON by default
    if os.environ.get("FONT_SMOOTHING", True):
        driver.execute_script(
            'document.querySelector("body").style.textShadow = "0px 0px 1px rgba(0,0,0,.7)"'
        )

    post_coordinates = PostCoordinates(
        x=target_element.location["x"],
        y=target_element.location["y"],
    )

    post_dimensions = PostDimensions(
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
        post_dimensions=post_dimensions,
        post_coordinates=post_coordinates,
        cropped=False,
    )
