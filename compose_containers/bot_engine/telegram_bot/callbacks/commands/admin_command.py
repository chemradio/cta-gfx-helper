from telegram import Update
from telegram.ext import ContextTypes

from telegram_bot.callbacks.admin_callbacks.ensure_admin import ensure_admin
from telegram_bot.callbacks.admin_callbacks.list_users_to_admin import (
    list_users_to_admin,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder


async def admin_panel_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = parse_user_id(update)
    if not await ensure_admin(user_id):
        return

    return await Responder.admin_panel.admin_panel(user_id)
