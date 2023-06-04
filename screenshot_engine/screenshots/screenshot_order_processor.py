import asyncio
import threading

from container_interation.edit_order_db import mark_order_screenshots
from container_interation.gather_orders import get_ready_to_screenshot_order
from container_interation.post_result_to_storage_unit import store_result
from screenshots.capture_screenshots import capture_screenshots
from utils.cleanup_assets import cleanup_order


async def process_screenshot_orders():
    while True:
        print("Getting ready for screenshoting orders")
        order = get_ready_to_screenshot_order()
        print(f"Current screenshot order = {order}")
        if not order:
            break

        screenshots_processed_order = capture_screenshots(order)
        store_result(screenshots_processed_order)
        mark_order_screenshots(screenshots_processed_order)
        cleanup_order(order)


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
