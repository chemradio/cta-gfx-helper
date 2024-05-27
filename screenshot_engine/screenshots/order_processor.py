import config

# from container_interation.edit_order_db import mark_order_screenshots
from screenshots.logic.type_classes.screenshot import ScreenshotResults
from shared.orders.screenshot_order import ScreenshotOrder
from screenshots.capture_processor import attempt_capture
from shared.database.db import db_handler
from shared.orders.order_base import OrderStatus


def process_screenshot_order(order: ScreenshotOrder):
    print(f"Current screenshot order = {order}", flush=True)
    db_handler.add_order(order.to_dict())
    screenshot_results = attempt_capture(order.screenshot_link)
    order.results = screenshot_results

    # store files
    if screenshot_results.success:
        with open(config.SCREENSHOT_FOLDER / order.bg_filename, "wb") as f:
            f.write(screenshot_results.background.content.getvalue())

        if screenshot_results.two_layer:
            with open(config.SCREENSHOT_FOLDER / order.fg_filename, "wb") as f:
                f.write(screenshot_results.foreground.content.getvalue())

        db_handler.update(
            order.order_id,
            {
                "status": OrderStatus.DONE,
                "output": [
                    file for file in [order.bg_filename, order.fg_filename] if file
                ],
            },
        )
    else:
        db_handler.update(order.order_id, {"status": OrderStatus.FAILED})


    # mark_order_screenshots(order)

    return order
