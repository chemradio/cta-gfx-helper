import time
import threading
from database.db import db_handler
from engines.sender_engine import send_video_order
from engines.video_gfx_html.video_wizard import create_video_gfx


import logging
logger_gfx = logging.getLogger(__name__)
logger_gfx.setLevel(logging.DEBUG)
logging_gfx_formatter = logging.Formatter('%(asctime)s: %(name)s: %(message)s')
logging_gfx_file_handler = logging.FileHandler(f'./logs/{__name__}.log', mode='w+')
logging_gfx_file_handler.setLevel(logging.DEBUG)
logging_gfx_file_handler.setFormatter(logging_gfx_formatter)
logging_gfx_stream_handler = logging.StreamHandler()
logging_gfx_stream_handler.setFormatter(logging_gfx_formatter)
logger_gfx.addHandler(logging_gfx_file_handler)
logger_gfx.addHandler(logging_gfx_stream_handler)


def render_video_orders():
    logger_gfx.debug("THREAD: render_video_orders accessed")
    def renderer():
        # time.sleep(30)  # initial startup to allow screenshots to be captured
        while db_handler.get_unrendered_orders():
            logger_gfx.debug("GFX Renderer started")
            time.sleep(1)
            order = db_handler.get_unrendered_orders()[0]

            # launch html-based animation creator
            create_video_gfx(order=order)

            db_handler.update_doc_db_parameters(doc_id=order.doc_id, parameters={'stage':'sending', 'start_render_timestamp': time.time()})
            logger_gfx.debug("GFX Renderer accessed SENDER Engine")
            send_video_order(order)
            
            time.sleep(10)
        return

    for thread in threading.enumerate():
        if 'render_video_orders_thread' in thread.name:
            logger_gfx.debug("THREAD: render_video_orders already runnung")
            return False

    render_video_orders_thread = threading.Thread(target=renderer, args=(), name='render_video_orders_thread')
    render_video_orders_thread.start()
    logger_gfx.debug("THREAD: render_video_orders started")
    return True
