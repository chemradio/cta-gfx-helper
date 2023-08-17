import config
from screenshots.logic.helpers.parse_link_type import parse_link_type
from screenshots.logic.screenshooter import Screenshooter


def prep_for_screenshots(url: str) -> dict:
    clean_original_url, domain, two_layer = parse_link_type(url=url)

    return {
        "original_url_cleaned": clean_original_url,
        "two_layer": two_layer,
        "foreground_url": str,
        "background_url": str,
        "login_required": bool,
        "domain": str,
    }


# def capture_screenshots(order: dict) -> dict:
#     # parse link type
#     link_type, clean_url = parse_link_type(order["link"])
#     order.update({"link_type": link_type, "link": clean_url})

#     attempts = config.SCREENSHOT_ATTEMPTS
#     while attempts:
#         screenshooter = Screenshooter()
#         bg_path = config.SCREENSHOT_FOLDER / order.get("background_name")
#         fg_path = config.SCREENSHOT_FOLDER / order.get("foreground_name")

#         try:
#             screenshots_ready = screenshooter.capture_screenshot(
#                 url=order["link"], bg_path=bg_path, fg_path=fg_path
#             )
#             order["screenshots_ready"] = screenshots_ready
#             break
#         except Exception as e:
#             print(
#                 f"Screenshooting failed. Attempt {attempts}/{config.SCREENSHOT_ATTEMPTS}"
#             )
#             print(e)
#             attempts -= 1
#     else:
#         order["error"] = "True"
#         order["error_type"] = "screenshot_error"

#     return order
