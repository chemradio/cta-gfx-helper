import os

import requests

from screenshots.logic.type_classes.screenshot import Screenshot, ScreenshotResults

STORAGE_UNIT_NAME = os.getenv("STORAGE_UNIT_NAME", "storage_unit")
STORAGE_UNIT_PORT = os.getenv("STORAGE_UNIT_PORT", 9010)
STORAGE_UNIT_ENDPOINT = f"http://{STORAGE_UNIT_NAME}:{STORAGE_UNIT_PORT}/file"


def store_result(screenshot_results: ScreenshotResults):
    print("about to store screenshot results in storage unit", flush=True)
    print(f"{screenshot_results=}", flush=True)
    print(f"{screenshot_results.background=}", flush=True)
    print(f"{screenshot_results.foreground=}", flush=True)
    print(f"{screenshot_results.two_layer=}", flush=True)
    if screenshot_results.background:
        store_screenshot(screenshot_results.background)

    if screenshot_results.foreground:
        store_screenshot(screenshot_results.foreground)


def store_screenshot(screenshot: Screenshot) -> None:
    print("Screenshooter storing file:", screenshot.filename)
    response = requests.post(
        STORAGE_UNIT_ENDPOINT,
        files={
            "upload_file": (
                screenshot.filename,
                screenshot.content.getvalue(),
                "image/png",
            )
        },
    )
    # assert response.status_code == 200
