from config import SCREENSHOT_ATTEMPTS
from screenshots.parse_link_type import parse_link_type
from screenshots.screenshooter import Screenshooter


def capture_screenshots(order: dict) -> dict:
    # parse link type
    link_type, clean_url = parse_link_type(order["link"])
    order.update({"link_type": link_type, "link": clean_url})

    screenshooter = Screenshooter()
    attempts = SCREENSHOT_ATTEMPTS

    while attempts:
        try:
            screenshot_dict = screenshooter.capture_screenshot(url=order["link"])
            order.update(
                {
                    "fg_path": screenshot_dict["fg_path"],
                    "bg_path": screenshot_dict["bg_path"],
                    "screenshots_ready": True,
                }
            )

            next_status_map = {
                "only_screenshots": "ready_to_send",
                "video_auto": "video_gfx_pending",
            }

            order.update({"current_stage": next_status_map[order["request_type"]]})
            break
        except Exception as e:
            print(f"Screenshooting failed. Attempt {attempts}/{SCREENSHOT_ATTEMPTS}")
            print(e)
            attempts -= 1
    else:
        order.update({"status": "error", "current_stage": "screenshot_error"})
    return order
