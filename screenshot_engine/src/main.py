from pathlib import Path

from screenshots.screenshot_capture.parse_capture_screenshots import (
    parse_capture_screenshots,
)

from shared.models.operator_results import OperatorResults
from shared.models.output_file import OperatorOutputFile

from .screenshot_config import SCREENSHOT_ATTEMPTS


def capture_screenshots(url: str, output_path: Path) -> OperatorResults: ...


def main_capture(order: dict) -> OperatorResults:
    url = order["screenshot_link"]

    # attempt capture
    success = False
    error = False
    error_message = ""
    operator_output = None

    for attempt in range(SCREENSHOT_ATTEMPTS):
        try:
            capture_results = parse_capture_screenshots(url)
            success = True
            break

        except Exception as e:
            print(f"Attempt: {attempt} Failed to screenshoot url: {url}.", flush=True)
            success = False
            error = True
            error_message = str(e)
            print(error_message, flush=True)

    if success:
        # extract output from ScreenshotResults object
        operator_output: list[OperatorOutputFile] = list()
        ...
    else:
        print(f"Screenshooting failed after {SCREENSHOT_ATTEMPTS} attempts.")

    return OperatorResults(
        success=success,
        operator_output=operator_output,
        error=error,
        error_message=error_message,
    )
