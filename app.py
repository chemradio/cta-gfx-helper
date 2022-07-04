import os
import time
import telegram
from engines.utils import clear_assets_folder
from engines.block_logger import block_logger_thread
from database.db import db_handler
from engines.telegram_bot_thread import bot_thread


os.system("clear")


if __name__ == "__main__":
    db_handler.start_terminate_all_active_sessions()
    clear_assets_folder()
    
    # run_adobe : str = input('Do you want to start Adobe Apps? (Y/n): ')
    # if run_adobe.lower() == 'y':
    #     print('Starting...')
    #     os_script.start_adobe_apps()    

    # from utils.auth_chrome import auth_chrome
    # auth_chrome()

    db_handler.log_event('run', 'bot_launch')
    block_logger_thread()
    
    while True:
        try:
            bot_thread()
        except telegram.error.Conflict:
            print('caught CONFLICT')
            time.sleep(10)
        except:
            db_handler.log_error('network_timeout')
            time.sleep(10)