from typing import Literal
import interlinks
import time
import threading
from database.db import db_handler
from engines.telegram_bot.bot_instance import bot
from engines.screenshots.screenshooter import Screenshooter
from engines.video_gfx_engines import render_video_orders
from engines.sender_engine import send_ready_orders
from telegram import ReplyKeyboardRemove


def process_screenshot_orders(link_list: list[str] = []) -> None:
    screenshooter = Screenshooter()
    def capturer():
        
        # for testing
        # if link_list:
        #     uncaptured_screenshots = link_list
        # else:
        #     uncaptured_screenshots = link_list

        while db_handler.get_uncaptured_screenshots():
            time.sleep(1)
            order = db_handler.get_uncaptured_screenshots()[0]

            for attempt in range(1, interlinks.SCREENSHOT_ATTEMPTS + 1):
                try:
                    screenshot_dict = screenshooter.capture_screenshot(url=order["link"])
                    break
                except:
                    print(f"Screenshooting failed. Attempt {attempt}/{interlinks.SCREENSHOT_ATTEMPTS}")
                    attempt += 1
            else:
                bot.send_message(
                    chat_id=order["chat_id"],
                    text="Произошла ошибка захвате скриншотов. Пожалуйста, проверь ссылку и оформи новый заказ через /start. Возможно это ссылка на закрытый профиль.",
                    reply_markup=ReplyKeyboardRemove(),
                )
                db_handler.update_doc_db_parameters(
                    doc_id=order.doc_id,
                    parameters={"status": "error_screenshot_terminated"},
                )
                return

            # update db
            update_dict = screenshot_dict
            update_dict["screenshots_ready"] = True
            if order["request_type"] == "only_screenshots":
                update_dict["stage"] = "sending"
            else:
                update_dict["stage"] = "screenshots_captured"
            db_handler.update_doc_db_parameters(doc_id=order.doc_id, parameters=update_dict)

            # start video thread
            if order["request_type"] == "video_auto":
                render_video_orders()
            else:
                send_ready_orders()
            

    for thread in threading.enumerate():
        if "capture_screenshots_orders_thread" in thread.name:
            return False

    capture_screenshots_orders_thread = threading.Thread(
        target=capturer, args=(), name="capture_screenshots_orders_thread"
    )
    capture_screenshots_orders_thread.start()
    return True
