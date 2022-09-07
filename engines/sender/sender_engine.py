import interlinks
import time
import re
import os
import threading
from engines.telegram_bot.bot_instance import bot
from database.db import db_handler
from telegram import ReplyKeyboardRemove


import logging
logger_sender = logging.getLogger(__name__)
logger_sender.setLevel(logging.DEBUG)
logging_sender_formatter = logging.Formatter('%(asctime)s: %(name)s: %(message)s')
# logging_sender_file_handler = logging.FileHandler(f'./logs/{__name__}.log', mode='w+')
# logging_sender_file_handler.setLevel(logging.DEBUG)
# logging_sender_file_handler.setFormatter(logging_sender_formatter)
logging_sender_stream_handler = logging.StreamHandler()
logging_sender_stream_handler.setFormatter(logging_sender_formatter)
# logger_sender.addHandler(logging_sender_file_handler)
logger_sender.addHandler(logging_sender_stream_handler)



def ame_log_parser(filename):
    logger_sender.debug("AMELOG PARSER: Started")
    try:
        amelog_file = open(interlinks.ame_log_file, 'rb')
        logger_sender.debug("AMELOG PARSER: AME Log file successfully opened")
    except FileNotFoundError:
        logger_sender.debug("AMELOG PARSER: Can't opent AME log file. It doesn't exist")
        return False

    amelog = amelog_file.read()
    decoded = amelog.decode('utf-16le', 'ignore')
    amelog_file.close()

    regex = r"\s.+\s.+\s.+\s.+\s.+\s.+"
    matches = re.findall(filename + regex, decoded)

    if matches:
        if 'File Successfully Encoded' in matches[-1]:
            logger_sender.debug(f"AMELOG PARSER: Amelog parser found {filename} in log file. And it's status is: {'File Successfully Encoded'}")
            return 'success'

        elif 'Encoding Failed' in matches[-1]:
            logger_sender.debug(f"AMELOG PARSER: Amelog parser found {filename} in log file. And it's status is: {'Encoding failed'}")
            return 'failed'

        else:
            logger_sender.debug(f"AMELOG PARSER: Amelog parser found {filename} in log file. And it's status is: {'Pending'}")
            return 'unknown'

    else:
        logger_sender.debug(f"AMELOG PARSER: Amelog parser couldn't find {filename} in log file.")
        return False


def send_single_order(order):
    order_doc_id = order.doc_id
    if order['request_type'] == 'only_screenshots':
        bg_screenshot = open(order["bg_path"], 'rb')
        logger_sender.debug("Sending bg_screenshot out")
        bot.send_document(order['chat_id'], bg_screenshot, reply_markup=ReplyKeyboardRemove(), reply_to_message_id=order['results_message_id'], timeout=300)
        if order['is_two_layer']:
            fg_screenshot = open(order["fg_path"], 'rb')
            logger_sender.debug("Sending fg_screenshot out")
            bot.send_document(order['chat_id'], fg_screenshot, reply_markup=ReplyKeyboardRemove(), reply_to_message_id=order['results_message_id'], timeout=300)

        db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={
            'stage': 'completed',
            'status': 'success'
        })

    elif order['request_type'] == 'video_auto' or 'video_files':
        pass
        # render_file_path = f"{interlinks.render_output_path}/{order['render_filename']}"
        # render_file_name = order['render_filename']

        # amelog_result = ame_log_parser(render_file_name)

        # if amelog_result == 'success':
        #     with open(render_file_path, 'rb') as binarified_file:
        #         try:
        #             logger_sender.debug("Sending video-gfx out")
        #             bot.send_document(chat_id=order['chat_id'], document=binarified_file, caption="При необходимости подложи озвучку.", reply_to_message_id=order['results_message_id'], allow_sending_without_reply=True, reply_markup=ReplyKeyboardRemove(), timeout=300)
        #         except:
        #             logger_sender.exception("Sending video-gfx FAILED")
        #             db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={'status': 'send_error'})
        #     db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={'status': 'success', 'stage':'completed'})

        # elif amelog_result == 'failed' or amelog_result == 'unknown':
        #     bot.send_message(chat_id=order['chat_id'], text= 'Произошла ошибка при экспорте видео-файла. Пожалуйста, начни заказ заново.', reply_markup=ReplyKeyboardRemove())
        #     db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={'status':'error_fail_render'})

        # elif amelog_result == False:
        #     pass


def send_video_order(order):
    order_doc_id = order.doc_id
    render_file_path = f"{interlinks.RENDER_OUTPUT_PATH}/{order['render_filename']}"
    render_file_name = order['render_filename']

    with open(render_file_path, 'rb') as binarified_file:
        try:
            logger_sender.debug("Sending video-gfx out")
            bot.send_document(chat_id=order['chat_id'], document=binarified_file, caption="При необходимости подложи озвучку.", reply_to_message_id=order['results_message_id'], allow_sending_without_reply=True, reply_markup=ReplyKeyboardRemove(), timeout=300)
            db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={'status': 'success', 'stage':'completed'})
            return True
        except:
            logger_sender.exception("Sending video-gfx FAILED")
            db_handler.update_doc_db_parameters(doc_id=order_doc_id, parameters={'status': 'send_error'})
            return False


def send_ready_orders():
    logger_sender.debug('THREAD: File Sender Thread Accessed.')
    def sender():
        # time.sleep(30)
        while db_handler.get_unsent_orders():
            time.sleep(1)
            for order in db_handler.get_unsent_orders():
                send_single_order(order)
            time.sleep(5)
        return

    for thread in threading.enumerate():
        if 'orders_sender_thread' in thread.name:
            logger_sender.debug("THREAD: File Sender already runnung")
            return False

    orders_sender_thread = threading.Thread(target=sender, args=(), name='orders_sender_thread')
    orders_sender_thread.start()
    logger_sender.debug("THREAD: File Sender thread started")
    return True


