import os
import time
import telegram
from os_scripts.os_script_handler import os_script
from interlinks import BOT_TOKEN
from handlers.inline_handler import inline_button_handler
from handlers.back_command_handler import back_handler
from handlers.exit_handler import exit_handler
from handlers.register_handler import register_handler
from handlers.help_handler import help_handler
from handlers.attachment_handler import attachment_handler
from handlers.text_handler import main_handler
from handlers.start_handlers import (
    start,
    start_only_screenshots,
    start_video_auto_production,
    start_video_files_production,
    start_readtime,
)
from handlers.admin_commands import (
    register_requests_handler,
    registered_users_handler,
    blocked_users_handler,
    recent_orders,
    processing_orders,
    active_orders,
    terminate_sessions,
    restart_adobe_apps,
    start_adobe_apps,
    quit_adobe_apps,
    check_adobe_running,
    check_chrome_running,
    quit_chrome,
    clear_bot_cache,
    cache_size,
    send_announcement,
)

from engines.utils import clear_assets_folder
from engines.block_logger import block_logger_thread
from database.db import db_handler
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)





os.system("clear")


def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("video_auto", start_video_auto_production))
    dispatcher.add_handler(CommandHandler("video_files", start_video_files_production))
    dispatcher.add_handler(CommandHandler("only_screenshots", start_only_screenshots))
    dispatcher.add_handler(CommandHandler("readtime", start_readtime))
    dispatcher.add_handler(CommandHandler("exit", exit_handler))
    dispatcher.add_handler(CommandHandler("register", register_handler))
    dispatcher.add_handler(CommandHandler("help", help_handler))
    dispatcher.add_handler(CommandHandler("register_requests", register_requests_handler))
    dispatcher.add_handler(CommandHandler("registered_users", registered_users_handler))
    dispatcher.add_handler(CommandHandler("blocked_users", blocked_users_handler))
    dispatcher.add_handler(CommandHandler("back", back_handler))
    dispatcher.add_handler(CommandHandler("recent_orders", recent_orders))
    dispatcher.add_handler(CommandHandler("terminate_sessions", terminate_sessions))
    dispatcher.add_handler(CommandHandler("processing_orders", processing_orders))
    dispatcher.add_handler(CommandHandler("active_orders", active_orders))
    dispatcher.add_handler(CommandHandler("restart_adobe_apps", restart_adobe_apps))
    dispatcher.add_handler(CommandHandler("start_adobe_apps", start_adobe_apps))
    dispatcher.add_handler(CommandHandler("quit_adobe_apps", quit_adobe_apps))
    dispatcher.add_handler(CommandHandler("check_adobe_running", check_adobe_running))
    dispatcher.add_handler(CommandHandler("clear_bot_cache", clear_bot_cache))
    dispatcher.add_handler(CommandHandler("check_chrome_running", check_chrome_running))
    dispatcher.add_handler(CommandHandler("quit_chrome", quit_chrome))
    dispatcher.add_handler(CommandHandler("cache_size", cache_size))
    dispatcher.add_handler(CommandHandler("send_announcement", send_announcement))

    dispatcher.add_handler(MessageHandler(Filters.attachment, attachment_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, main_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    db_handler.start_terminate_all_active_sessions()
    clear_assets_folder()

    # check for logs folder existence
    # os_script.start_adobe_apps()

    db_handler.log_event('run', 'bot_launch')
    block_logger_thread()
    
    while True:
        try:
            main()
            
        except telegram.error.Conflict:
            print('caught CONFLICT')
            time.sleep(10)
        except:
            db_handler.log_error('network_timeout')
            time.sleep(10)