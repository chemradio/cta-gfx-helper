import interlinks
from database.db import db_handler
from telegram import (
    ReplyKeyboardRemove,
    Update,
    ParseMode,
)
from telegram.ext import (
    CallbackContext,
)

from engines.telegram_bot.legacy_handlers.decorators import logger_bot


################################################################
def exit_handler(update: Update, _: CallbackContext) -> None:
    logger_bot.debug(
        f"exit - First name: {update.message.from_user.first_name} {update.message.from_user.id}"
    )
    db_handler.terminate_all_sessions(update.message.from_user.id)
    update.message.reply_text(
        interlinks.stage_texts["common"]["sessions_terminated_start"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )
    return