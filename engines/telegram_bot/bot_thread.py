from telegram.ext import Updater
import telegram
import time
import threading
from database.db import db_handler

from interlinks import BOT_TOKEN
from engines.telegram_bot.legacy_handlers.inline_handler import inline_button_handler
from engines.telegram_bot.legacy_handlers.back_command_handler import back_handler
from engines.telegram_bot.legacy_handlers.exit_handler import exit_handler
from engines.telegram_bot.legacy_handlers.register_handler import register_handler
from engines.telegram_bot.legacy_handlers.help_handler import help_handler
from engines.telegram_bot.legacy_handlers.attachment_handler import attachment_handler
from engines.telegram_bot.legacy_handlers.text_handler import main_handler
from engines.telegram_bot.legacy_handlers.start_handlers import (
    start,
    start_only_screenshots,
    start_video_auto_production,
    start_video_files_production,
    start_readtime,
)
from engines.telegram_bot.legacy_handlers.admin_commands import (
    register_requests_handler,
    registered_users_handler,
    blocked_users_handler,
    recent_orders,
    processing_orders,
    active_orders,
    terminate_sessions,
    clear_bot_cache,
    cache_size,
    send_announcement,
)

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)


def bot_updater_dispatcher_legacy() -> Updater:
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
    # dispatcher.add_handler(CommandHandler("restart_adobe_apps", restart_adobe_apps))
    # dispatcher.add_handler(CommandHandler("start_adobe_apps", start_adobe_apps))
    # dispatcher.add_handler(CommandHandler("quit_adobe_apps", quit_adobe_apps))
    # dispatcher.add_handler(CommandHandler("check_adobe_running", check_adobe_running))
    dispatcher.add_handler(CommandHandler("clear_bot_cache", clear_bot_cache))
    # dispatcher.add_handler(CommandHandler("check_chrome_running", check_chrome_running))
    # dispatcher.add_handler(CommandHandler("quit_chrome", quit_chrome))
    dispatcher.add_handler(CommandHandler("cache_size", cache_size))
    dispatcher.add_handler(CommandHandler("send_announcement", send_announcement))

    dispatcher.add_handler(MessageHandler(Filters.attachment, attachment_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, main_handler))

    updater.start_polling()
    updater.idle()


# def bot_updater_dispatcher_v2():
#     updater = Updater(BOT_TOKEN)
#     dispatcher = updater.dispatcher

#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(CommandHandler("exit", exit_handler))
#     dispatcher.add_handler(CommandHandler("help", help_handler))

#     dispatcher.add_handler(CallbackQueryHandler(inline_button_handler))

#     # dispatcher.add_handler(MessageHandler(Filters.text, main_handler), MessageHandler(None, ))

#     updater.start_polling()
#     updater.idle()


def bot_safe_loop() -> None:
    while True:
        try:
            bot_updater_dispatcher_legacy()
        except telegram.error.Conflict:
            print('Telegram Conflict')
            time.sleep(10)
        except Exception as e:
            print(e)
            # print('Network timeout')
            db_handler.log_error('network_timeout')
            time.sleep(10)



def bot_thread_launcher() -> None:
    def bot_thread():
        while True:
            try:
                print('starting to poll!!!!\n\n\n')
                # polling_bot(updater)
                bot_updater_dispatcher_legacy()
                # while True:
                #     time.sleep(1)
            except telegram.error.Conflict:
                print('caught CONFLICT')
                time.sleep(10)
            except:
                print('Network timeout')
                db_handler.log_error('network_timeout')
                time.sleep(10)

    for thread in threading.enumerate():
        if "telegram_bot_thread" in thread.name:
            return False

    telegram_bot_thread = threading.Thread(
        target=bot_thread, args=(), name="telegram_bot_thread"
    )
    telegram_bot_thread.start()
    return True
