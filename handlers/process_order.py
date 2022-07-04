import time
from database.db import db_handler
from engines.video_gfx_engines import render_video_orders
# from engines.screenshot_capture import process_screenshot_orders
from engines.screenshots.screenshot_order_processor import process_screenshot_orders


def process_order(db_query):
    # if all files are already provided - begin AE render
    if db_query["request_type"] == "video_files":
        db_handler.update_doc_db_parameters(
            doc_id=db_query.doc_id,
            parameters={
                "chat_id": db_query["telegram_id"],
                "stage": "screenshots_captured",
            },
        )
        render_video_orders()
        return

    # if screenshot capture is required - do it first.
    # AE render is triggered automatically after screenshots are captured
    else:
        db_handler.set_user_stage(db_query["telegram_id"], "screenshots")
        db_handler.update_doc_db_parameters(
            doc_id=db_query.doc_id,
            parameters={"chat_id": db_query["telegram_id"], "stage": "screenshots"},
        )
        process_screenshot_orders()
        return
