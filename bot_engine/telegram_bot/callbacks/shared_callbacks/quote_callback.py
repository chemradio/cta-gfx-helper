from typing import Callable

from telegram import Update
from telegram.ext import ContextTypes

from container_interaction.process_string_api import process_quote_string
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder


async def quote_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE, caller: Callable = None
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    try:
        if stage == "quote_enabled":
            if update.callback_query.data not in ["quote_enabled", "quote_disabled"]:
                raise Exception()

            await update.callback_query.answer(cache_time=180)

            if update.callback_query.data == "quote_enabled":
                user_data.update({"quote_enabled": True, "stage": "quote_text"})
                return await Responder.quote.ask_quote_text(user_id)
            else:
                user_data.update({"quote_enabled": False, "stage": "quote_passed"})
                return await caller(update, context)

        if stage == "quote_text":
            message_text = update.message.text
            if not message_text:
                raise Exception()

            user_data.update(
                {
                    "quote_text": await process_quote_string(message_text),
                    "stage": "quote_author_enabled",
                }
            )
            return await Responder.quote.ask_quote_author_enabled(user_id)

        if stage == "quote_author_enabled":
            if update.callback_query.data not in [
                "quote_author_enabled",
                "quote_author_disabled",
            ]:
                raise Exception()

            await update.callback_query.answer(cache_time=60)
            # await update.callback_query.edit_message_text(
            #     text=update.callback_query.message.text
            # )

            if update.callback_query.data == "quote_author_enabled":
                user_data.update(
                    {"quote_author_enabled": True, "stage": "quote_author_text"}
                )
                return await Responder.quote.ask_quote_author_text(user_id)
            else:
                user_data.update(
                    {"quote_author_enabled": False, "stage": "quote_passed"}
                )
                return await caller(update, context)

        if stage == "quote_author_text":
            message_text = update.message.text
            if not message_text:
                raise Exception()

            user_data.update(
                {
                    "quote_author_text": await process_quote_string(message_text),
                    "stage": "quote_passed",
                }
            )
            return await caller(update, context)

    except Exception as e:
        print(str(e), flush=True)
        return await Responder.errors.gp_error(user_id, str(e))
