from .bot_instance import BOT_TOKEN
from .all_handler import AllHandler
from .callbacks.main_callback.main_dispatcher_callback import dispatcher_callback
from telegram.ext import Application, CommandHandler


def bot_application_v20():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(AllHandler(dispatcher_callback))
    application.run_polling()
