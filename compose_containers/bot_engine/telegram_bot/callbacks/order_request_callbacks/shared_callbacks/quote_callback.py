import json
from typing import Callable

from telegram import Update
from telegram.ext import ContextTypes

from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder
from py_gfxhelper_lib.miscellaneous.string_cleaner import cleanup_string


async def quote_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE, caller: Callable = None
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    try:

        if stage == "quote_enabled":
            try:
                if update.message.text:
                    user_data.update({"stage": "quote_text"})
                    return await quote_callback(update, context, caller)
            except:
                ...
            if update.callback_query.data not in ["quote_enabled", "quote_disabled"]:
                raise Exception()

            await update.callback_query.answer(cache_time=180)

            if update.callback_query.data == "quote_enabled":
                user_data.update({"stage": "quote_text"})
                return await Responder.quote.ask_quote_text(user_id)
            else:
                user_data.update({"stage": "quote_passed"})
                return await caller(update, context)

        if stage == "quote_text":
            message_text = update.message.text
            if not message_text:
                raise Exception()

            try:
                user_data.update(
                    {
                        "quote_text": cleanup_string(message_text),
                        "stage": "quote_author_enabled",
                    }
                )
                return await Responder.quote.ask_quote_author_enabled(user_id)
            except Exception as e:
                return await Responder.errors.custom_error(user_id, str(e))

        if stage == "quote_author_enabled":
            try:
                if update.message.text:
                    user_data.update({"stage": "quote_author_text"})
                    return await quote_callback(update, context, caller)
            except:
                ...

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
                user_data.update({"stage": "quote_author_text"})
                return await Responder.quote.ask_quote_author_text(user_id)
            else:
                user_data.update({"stage": "quote_passed"})
                return await caller(update, context)

        if stage == "quote_author_text":
            message_text = update.message.text
            if not message_text:
                raise Exception()
            try:
                user_data.update(
                    {
                        "quote_author_text": cleanup_string(message_text),
                        "stage": "quote_passed",
                    }
                )
                return await caller(update, context)
            except Exception as e:
                return await Responder.errors.custom_error(user_id, str(e))

    except Exception as e:
        print(str(e), flush=True)
        return await Responder.errors.gp_error(user_id, str(e))
