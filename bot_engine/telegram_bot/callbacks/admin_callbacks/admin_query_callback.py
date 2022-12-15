from telegram import Update
from telegram.ext import ContextTypes

from container_interaction.users_db import allow_user, block_user, pend_user
from telegram_bot.responders.main_responder import Responder


async def admin_query_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    update_dict = update.to_dict()
    callback_query = update_dict.get("callback_query")
    if callback_query:
        await update.callback_query.answer(cache_time=180)
        data = update.callback_query.data

        if "approve_" in data:
            applicant_id = int(data.split("approve_")[1])
            await allow_user(applicant_id)
            await update.callback_query.edit_message_text(
                text=update.callback_query.message.text.split("\n")[2] + "\nApproved"
            )
            await Responder.register_user.register_approved(applicant_id)
            return True

        if "block_" in data:
            applicant_id = int(data.split("block_")[1])
            await block_user(applicant_id)
            await update.callback_query.edit_message_text(
                text=update.callback_query.message.text.split("\n")[2] + "\nBlocked"
            )
            return True

        if "pend_" in data:
            applicant_id = int(data.split("pend_")[1])
            await pend_user(applicant_id)
            await update.callback_query.edit_message_text(
                text=update.callback_query.message.text.split("\n")[2] + "\nPending"
            )
            return True
    return False
