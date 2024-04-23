import config
from screenshots.logic.screenshooter import capture_screenshots
from screenshots.logic.type_classes.screenshot import ScreenshotResults


def capture_processor(url: str) -> ScreenshotResults:
    error_message = ''
    capture_attempts = config.SCREENSHOT_ATTEMPTS
    while capture_attempts:
        try:
            return capture_screenshots(url)
        except Exception as e:
            capture_attempts -= 1
            print(
                f"Failed to screenshoot url: {url}. Remaining attempts: {capture_attempts}",
                flush=True,
            )
            error_message = str(e)
            print(error_message, flush=True)
    else:
        print(f"Screenshooting failed after {config.SCREENSHOT_ATTEMPTS} attempts.")
        return ScreenshotResults(success=False, error_message=error_message)