import interlinks
from telegram import (
    Update,
)
from telegram.ext import (
    CallbackContext,
)


def help_handler(update: Update, _: CallbackContext) -> None:
    help_message_string = (
        interlinks.help_text + interlinks.admin_commands
        if update.message.from_user.id in interlinks.ADMIN_TELEGRAM_IDS
        else interlinks.help_text
    )
    update.message.reply_text(help_message_string)
    return