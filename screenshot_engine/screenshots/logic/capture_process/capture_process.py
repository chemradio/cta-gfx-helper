import base64
import json
import os
from io import BytesIO

from screenshots.logic.controllers.routines.screenshot_routines import (
    ScreenshotRoutines,
)
from screenshots.logic.type_classes.post_location_size import (
    PostCoordinates,
    PostDimensions,
)
from screenshots.logic.type_classes.screenshot import Screenshot
from screenshots.logic.type_classes.screenshot_role import ScreenshotRole
from selenium import webdriver


def capture_screenshot(
    driver: webdriver.Chrome | webdriver.Remote,
    role: ScreenshotRole = ScreenshotRole.FULL_SIZE,
) -> Screenshot:
    if role == ScreenshotRole.POST:
        target_element = ScreenshotRoutines.post_workflow(driver)
    elif role == ScreenshotRole.FULL_SIZE:
        target_element = ScreenshotRoutines.profile_workflow(driver)

    # optional font smoothing - ON by default
    if os.environ.get("FONT_SMOOTHING", True):
        driver.execute_script(
            'document.querySelector("body").style.textShadow = "0px 0px 1px rgba(0,0,0,1)"'
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
