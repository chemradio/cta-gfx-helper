import time
import config
from typing import Any, Callable
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.responders.main_responder import Responder
from container_interaction.users_db import (
    add_pending_user,
    allow_user,
    block_user,
    check_user_status,
)
from container_interaction.helpers import UserStatus
from telegram_bot.callbacks.register.auth_exceptions import (
    PendingUser,
    UnregisteredUser,
    BlockedUser,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import (
    parse_user_id,
)


async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update_dict = update.to_dict()
    callback_query = update_dict.get("callback_query")
    if callback_query:
        await update.callback_query.answer(cache_time=180)
        data = update.callback_query.data
        if "approve" in data:
            applicant_id = int(data.split("approve_")[1])
            await allow_user(applicant_id)
            await update.callback_query.edit_message_text(
                text=update.callback_query.message.text + "\nApproved"
            )
            return await Responder.register_user.register_approved(applicant_id)

        if "block" in data:
            applicant_id = int(data.split("block_")[1])
            await block_user(applicant_id)
            await update.callback_query.edit_message_text(
                text=update.callback_query.message.text + "\nBlocked"
            )
            return
