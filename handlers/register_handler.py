import interlinks
from database.db import db_handler
from telegram import (
    Update,
    ParseMode,
)
from telegram.ext import (
    CallbackContext,
)


from handlers.decorators import logger_bot

def register_handler(update: Update, _: CallbackContext) -> None:
    logger_bot.debug(
        f"New register request - {update.message.from_user.first_name} {update.message.from_user.id}"
    )
    if db_handler.add_pending_user(update=update):
        update.message.reply_text(
            interlinks.stage_texts["register_applied"], parse_mode=ParseMode.HTML
        )
    else:
        update.message.reply_text(
            interlinks.stage_texts["already_in_db"], parse_mode=ParseMode.HTML
        )
    return