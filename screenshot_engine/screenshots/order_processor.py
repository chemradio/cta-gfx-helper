import config
# from container_interation.edit_order_db import mark_order_screenshots
from container_interation.post_result_to_storage_unit import store_result
from screenshots.logic.screenshooter import capture_screenshots
from screenshots.logic.type_classes.screenshot import ScreenshotResults
# from utils.cleanup_assets import cleanup_order
from screenshots.logic.type_classes.screenshot import ScreenshotOrder
from screenshots.capture_processor import capture_processor


def process_screenshot_order(order: ScreenshotOrder):
    print(f"Current screenshot order = {order}", flush=True)
    screenshot_results = capture_processor(order.screenshot_link)
    order.results = screenshot_results
    
    if screenshot_results.success:
        with open(config.SCREENSHOT_FOLDER/order.bg_filename, "wb") as f:
            f.write(screenshot_results.background.content.getvalue())
        
        if screenshot_results.two_layer:
            with open(config.SCREENSHOT_FOLDER/order.fg_filename, "wb") as f:
                f.write(screenshot_results.foreground.content.getvalue())

    ...
    # mark_order_screenshots(order)
    # cleanup_order(order)

    return order

