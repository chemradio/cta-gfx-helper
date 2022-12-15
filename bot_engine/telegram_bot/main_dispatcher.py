from telegram.ext import Application, CommandHandler

from .all_handler import AllHandler
from .bot_instance import BOT_TOKEN
from .callbacks.main_callback.main_dispatcher_callback import dispatcher_callback


def bot_application_v20():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(AllHandler(dispatcher_callback))
    application.run_polling()
