import time
from datetime import datetime, timedelta, tzinfo
from database.db import db_handler
from pprint import pprint
import sys
import os
import threading
from engines.telegram_bot.legacy_handlers import status_utils
block_refresh_interval = 1


def block_logger() -> None:
    bot_version = status_utils.get_bot_version_git()
    while True:
        current_timestamp = time.time()
        current_time = datetime.now().strftime("%H:%M:%S")
        run_launch, run_error = status_utils.runtime_since_launch()

        processing_orders_list = db_handler.get_processing_orders()
        active_orders = db_handler.get_active_orders()

        active_orders_count = len(active_orders)
        processing_orders_count = len(processing_orders_list)
        active_users_list = set([order['first_name'] for order in active_orders])
        active_users_count = len(active_users_list)
        total_orders_today = db_handler.get_today_orders(True)
        network_errors = db_handler.get_errors('network_timeout')

        print_string = f"""
************************
__CTA GFX TELEGRAM BOT__
************************
ver.by.git {bot_version}

Status: Active
Current Time               : {current_time}
Runtime since launch       : {run_launch}
Runtime since last error   : {run_error}
________________________
Total Orders Today         : {total_orders_today}
Connection Timeout Errors  : {len(network_errors)}
________________________
Active Sessions            : {active_orders_count}
Orders Processing          : {processing_orders_count}
___
Active Users               : {active_users_count}
Active Users List          : {', '.join(active_users_list)}"""

        for id, order in enumerate(active_orders, start=1):
            start_timestamp = order.get('start_timestamp')
            session_duration = status_utils.dt_secs(current_timestamp - start_timestamp)
            session_template = f"""
________________________
SESSION {id}
User:             {order.get('first_name')}
Status:           {order.get('status')}
Stage:            {order.get('stage')}
Start Timestamp:  {status_utils.dt_secs(start_timestamp)}
Session Duration: {session_duration}
Request:          {order.get('request_type')}
Link:             {order.get('link')}
"""
            print_string += session_template


        print(print_string)
        
        # line_count = print_string.count('\n') + 1
        lines = print_string.split('\n')
        # longest_line = max(lines, key=len)
        time.sleep(block_refresh_interval)
        os.system('clear')






def block_logger_thread():
    for thread in threading.enumerate():
        if 'block_logger_thread' in thread.name:
            return False

    block_log_thread = threading.Thread(target=block_logger, args=(), name='block_logger_thread')
    block_log_thread.start()
    return True
