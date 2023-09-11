import asyncio
import threading

import config
from container_interation.edit_order_db import mark_order_screenshots
from container_interation.gather_orders import get_ready_to_screenshot_order
from container_interation.post_result_to_storage_unit import store_result
from screenshots.logic.screenshooter import capture_screenshots
from screenshots.logic.type_classes.screenshot import ScreenshotResults
from utils.cleanup_assets import cleanup_order


async def process_screenshot_orders():
    while True:
        print("Getting ready for screenshoting orders", flush=True)
        order = get_ready_to_screenshot_order()
        if not order:
            break
        print(f"Current screenshot order = {order}", flush=True)

        capture_attempts = config.SCREENSHOT_ATTEMPTS
        while capture_attempts:
            try:
                screenshot_results = capture_screenshots(order)
                if order["request_type"] == "video_files":
                    order["is_two_layer"] = True
                elif order["request_type"] == "video_auto":
                    order["is_two_layer"] = screenshot_results.two_layer

                order["screenshots_ready"] = True
                break
            except:
                print("Failed to capture screenshots from these urls:")
                print(order.get("link"))
                print(order.get("background_link"))
                capture_attempts -= 1
                continue
        else:
            print("Screenshooting failed.")
            screenshot_results = ScreenshotResults(success=False)
            order["screenshots_ready"] = False
            order["error"] = "True"
            order["error_type"] = "screenshot_error"

        if screenshot_results.success:
            store_result(screenshot_results)

        mark_order_screenshots(order)
        # cleanup_order(order)


def screenshooter_thread():
    thread_name = "screenshooter_thread"
    for thread in threading.enumerate():
        if thread_name in thread.name:
            print(f"Thread {thread_name} already running... Returning")
            return

    threading.Thread(
        target=asyncio.run,
        args=(process_screenshot_orders(),),
        name=thread_name,
    ).start()
