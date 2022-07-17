from os_scripts.os_script_handler import os_script
from database.db import db_handler
from engines.utils import clear_assets_folder
from engines.block_logger import block_logger_thread
from engines.screenshots.screenshot_webdriver import ScreenshotWebdriver


import os
os.system("clear")


def main():
    # cleanup previous run
    db_handler.start_terminate_all_active_sessions()
    clear_assets_folder()
    
    # run adobe apps
    run_adobe : str = input('Do you want to start Adobe Apps? (Y/n): ')
    if run_adobe.lower() == 'y':
        print('Starting...')
        os_script.start_adobe_apps()    

    # authenticate browser / dump cookies
    scwd = ScreenshotWebdriver()
    scwd.login_to_social()

    # start block logger
    block_logger_thread()

    # start telegram bot
    db_handler.log_event('run', 'bot_launch')
    bot_safe_loop()


if __name__ == "__main__":
    main()
