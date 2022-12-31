import config
from screenshots.parse_link_type import parse_link_type
from screenshots.screenshooter import Screenshooter


def capture_screenshots(order: dict) -> dict:
    # parse link type
    link_type, clean_url = parse_link_type(order["link"])
    order.update({"link_type": link_type, "link": clean_url})

    attempts = config.SCREENSHOT_ATTEMPTS
    while attempts:
        screenshooter = Screenshooter()
        bg_path = config.SCREENSHOT_FOLDER / order.get("background_name")
        fg_path = config.SCREENSHOT_FOLDER / order.get("foreground_name")

        try:
            screenshots_ready = screenshooter.capture_screenshot(
                url=order["link"], bg_path=bg_path, fg_path=fg_path
            )
            order["screenshots_ready"] = screenshots_ready
            break
        except Exception as e:
            print(
                f"Screenshooting failed. Attempt {attempts}/{config.SCREENSHOT_ATTEMPTS}"
            )
            print(e)
            attempts -= 1
    else:
        order["error"] = "True"
        order["error_type"] = "screenshot_error"

    return order
