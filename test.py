from pprint import pprint
from telegram.ext import Updater
from interlinks import BOT_TOKEN

from telegram.ext import (
    Updater,
    Handler,
    MessageHandler,
    InlineQueryHandler
    
)

from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple, TypeVar, Union


from telegram import Update
from telegram.utils.helpers import DefaultValue

from telegram.ext.utils.types import CCT



RT = TypeVar('RT')
from telegram.ext import (
    CallbackContext,
)

def all_handler(update: Update, context:CallbackContext):
    pprint(update.to_dict())
    pprint(dir(CallbackContext))
    print(context.dispatcher)

    return update.message.reply_text('catch')

UT = TypeVar('UT')


class AllHandler(Handler):
    def __init__(self, callback: Callable[[UT, CCT], RT], pass_update_queue: bool = False, pass_job_queue: bool = False, pass_user_data: bool = False, pass_chat_data: bool = False, run_async: Union[bool, DefaultValue] = ...):
        super().__init__(callback, pass_update_queue, pass_job_queue, pass_user_data, pass_chat_data, run_async)


    def check_update(
        self, update: object
    ) -> Optional[Union[bool, Tuple[List[str], Optional[Union[bool, Dict]]]]]:
        if isinstance(update, Update):
            return update
        return None







def bot_updater_dispatcher() -> Updater:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(AllHandler(all_handler))

    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("video_auto", start_video_auto_production))
    # dispatcher.add_handler(CommandHandler("video_files", start_video_files_production))
    # dispatcher.add_handler(CommandHandler("only_screenshots", start_only_screenshots))
    # dispatcher.add_handler(CommandHandler("readtime", start_readtime))
    # dispatcher.add_handler(CommandHandler("exit", exit_handler))
    # dispatcher.add_handler(CommandHandler("register", register_handler))
    # dispatcher.add_handler(CommandHandler("help", help_handler))
    # dispatcher.add_handler(CommandHandler("register_requests", register_requests_handler))
    # dispatcher.add_handler(CommandHandler("registered_users", registered_users_handler))
    # dispatcher.add_handler(CommandHandler("blocked_users", blocked_users_handler))
    # dispatcher.add_handler(CommandHandler("back", back_handler))
    # dispatcher.add_handler(CommandHandler("recent_orders", recent_orders))
    # dispatcher.add_handler(CommandHandler("terminate_sessions", terminate_sessions))
    # dispatcher.add_handler(CommandHandler("processing_orders", processing_orders))
    # dispatcher.add_handler(CommandHandler("active_orders", active_orders))
    # dispatcher.add_handler(CommandHandler("restart_adobe_apps", restart_adobe_apps))
    # dispatcher.add_handler(CommandHandler("start_adobe_apps", start_adobe_apps))
    # dispatcher.add_handler(CommandHandler("quit_adobe_apps", quit_adobe_apps))
    # dispatcher.add_handler(CommandHandler("check_adobe_running", check_adobe_running))
    # dispatcher.add_handler(CommandHandler("clear_bot_cache", clear_bot_cache))
    # dispatcher.add_handler(CommandHandler("check_chrome_running", check_chrome_running))
    # dispatcher.add_handler(CommandHandler("quit_chrome", quit_chrome))
    # dispatcher.add_handler(CommandHandler("cache_size", cache_size))
    # dispatcher.add_handler(CommandHandler("send_announcement", send_announcement))

    # dispatcher.add_handler(MessageHandler(Filters.attachment, attachment_handler))
    # dispatcher.add_handler(CallbackQueryHandler(inline_button_handler))
    # dispatcher.add_handler(MessageHandler(Filters.text, main_handler))

    updater.start_polling()
    updater.idle()      


bot_updater_dispatcher()