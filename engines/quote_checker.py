from logging import StringTemplateStyle
from interlinks import delegate_editor as editor
from interlinks import quote_checker as qcm
import time
import re
import threading
from engines.telegram_bot.bot_instance import bot
from database.db import db_handler
from telegram import ReplyKeyboardRemove


def check_quotes(edit: str = None):
    def checker(edited_text):
        # time.sleep(30)
        while db_handler.get_unchecked_quotes():
            # get first quote in queue
            quote = db_handler.get_unchecked_quotes()[0]

            stages = ["main", "text", "author", "final"]

            for stage in stages:
                if not quote[f"qc_{stage}_notification_sent"]:
                    bot.send_message(chat_id=editor, text=qcm[stage].format(""))
                else:
                    if not quote[f"qc_{stage}_notification_responded"]:
                        break
                    else:
                        ...

            # check if got a responses
            # "qc_main_notification_responded": False,
            # proceed to next
            # else:
            # break stop

            # QUOTE TEXT
            # check for quote text notification sent
            # "qc_quote_text_sent": False,
            # send if not sent already
            # else:
            # check if got a response
            # "qc_quote_text_received": False,
            # proceed to next
            # else:
            # break stop

            # QUOTE AUTHOR
            # check for quote author notification sent
            # "qc_quote_author_sent": False,
            # send if not sent already
            # else:
            # check if got a response
            # "qc_quote_author_received": False,
            # proceed to next
            # else:
            # break stop

            # FINAL CHECK / CONFIRMATION
            # check for final confirmation notification sent
            # "qc_final_confirmation_sent": False,
            # send if not sent already
            # else:
            # check if got a response
            # "qc_final_confirmation_responded": False,
            # quote checked = true
            # process order
            # continue to next quote
            # else:
            # break stop

            # check if quote was checked completely
            # change the status to next stage
            # process order()
            # proceed to the next quote

            # time.sleep(1)
            # for order in db_handler.get_unchecked_quotes():
            #     # aiai

            #     order_doc_id = order.doc_id
            #     if order['request_type'] == 'only_screenshots':
            #         bg_screenshot = open(order["bg_path"], 'rb')
            #         logger_sender.debug("Sending bg_screenshot out")
            #         bot.send_document(order['chat_id'], bg_screenshot, reply_markup=ReplyKeyboardRemove(), reply_to_message_id=order['results_message_id'], timeout=300)
            #         if order['is_two_layer']:
            #             fg_screenshot = open(order["fg_path"], 'rb')
            #             logger_sender.debug("Sending fg_screenshot out")
            #             bot.send_document(order['chat_id'], fg_screenshot, reply_markup=ReplyKeyboardRemove(), reply_to_message_id=order['results_message_id'], timeout=300)

            #         db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={
            #             'stage': 'completed',
            #             'status': 'success'
            #         })

            #     elif order['request_type'] == 'video_auto' or 'video_files':
            #         render_file_path = f"{config.render_output_path}/{order['render_filename']}"
            #         render_file_name = order['render_filename']
            #         amelog_result = ame_log_parser(render_file_name)

            #         if amelog_result == 'success':
            #             with open(render_file_path, 'rb') as binarified_file:
            #                 try:
            #                     logger_sender.debug("Sending video-gfx out")
            #                     bot.send_document(chat_id=order['chat_id'], document=binarified_file, caption="При необходимости подложи озвучку.", reply_to_message_id=order['results_message_id'], allow_sending_without_reply=True, reply_markup=ReplyKeyboardRemove(), timeout=300)
            #                 except:
            #                     logger_sender.exception("Sending video-gfx FAILED")
            #                     db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={'status': 'send_error'})
            #             db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={'status': 'success', 'stage':'completed'})

            #         elif amelog_result == 'failed' or amelog_result == 'unknown':
            #             bot.send_message(chat_id=order['chat_id'], text= 'Произошла ошибка при экспорте видео-файла. Пожалуйста, начни заказ заново.', reply_markup=ReplyKeyboardRemove())
            #             db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={'status':'error_fail_render'})

            #         elif amelog_result == False:
            #             pass

            # time.sleep(5)
        return

    for thread in threading.enumerate():
        if "quote_checker_thread" in thread.name:
            # logger_sender.debug("THREAD: File Sender already runnung")
            return False

    quote_checker_thread = threading.Thread(
        target=checker, args=(edit), name="quote_checker_thread"
    )
    quote_checker_thread.start()
    # logger_sender.debug("THREAD: File Sender thread started")
    return True
