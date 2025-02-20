from typing import Callable
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.responders.main_responder import Responder
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from py_gfxhelper_lib.miscellaneous.check_url import check_is_url

async def link_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE, caller: Callable = None
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data

    try:
        link = check_is_url(update.message.text)[0]
        user_data.update({"screenshot_link": link, "stage": "link_passed"})
        return await caller(update, context)

    except Exception as e:
        print(e)
        return await Responder.link.bad_link(user_id)

    