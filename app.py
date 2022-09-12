from database.db import db_handler
from engines.utils import clear_assets_folder
from engines.block_logger.block_logger import block_logger_thread
from engines.engine_tests import run_tests
from engines.telegram_bot.bot_thread import bot_safe_loop
from engines.video_gfx_html.html_server import start_httpd


# import os
# os.system("clear")


def main():
    # # cleanup previous run
    db_handler.start_terminate_all_active_sessions()
    clear_assets_folder()
    print('passed through cleaning assets')

    # create asset server
    start_httpd()
    print('passed through starting server')

    # run tests
    # run_tests() 

    
    # # authenticate browser / dump cookies
    # scwd = ScreenshotWebdriver(only_for_login=True)
    # try:
    #     scwd.login_to_social()
    # except:
    #     pass

    # start block logger
    # block_logger_thread()

    # start telegram bot
    db_handler.log_event('run', 'bot_launch')
    bot_safe_loop()


if __name__ == "__main__":
    main()
