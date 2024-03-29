from pprint import pprint
from telegram import Update
from telegram.ext import ContextTypes
from container_interaction.orders_db import add_order_to_db
from telegram_bot.callbacks.shared_callbacks.audio_callback import audio_callback
from telegram_bot.callbacks.shared_callbacks.link_callback import link_callback
from telegram_bot.callbacks.shared_callbacks.quote_callback import quote_callback
from telegram_bot.callbacks.shared_callbacks.results_callback import results_callback
from telegram_bot.responders.main_responder import Responder
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id


async def video_auto_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    # initialize order / ask LINK
    if stage == "start_order":
        user_data.update({"stage": "link"})
        return await Responder.link.ask_link(user_id)

    # handle LINK response
    if stage == "link":
        return await link_callback(update, context, video_auto_callback)

    # ask QUOTE
    if stage == "link_passed":
        user_data.update({"stage": "quote_enabled"})
        return await Responder.quote.ask_quote_enabled(user_id)

    # handle QUOTE responses
    if stage in [
        "quote_enabled",
        "quote_text",
        "quote_author_enabled",
        "quote_author_text",
    ]:
        return await quote_callback(update, context, video_auto_callback)

    # ask AUDIO
    if stage == "quote_passed":
        user_data.update({"stage": "audio_enabled"})
        return await Responder.audio.ask_audio_enabled(user_id)

    # handle AUDIO responses
    if stage in ["audio_enabled", "audio_file"]:
        return await audio_callback(update, context, video_auto_callback)

    # ask RESULTS
    if stage == "audio_passed":
        user_data.update({"stage": "results"})
        return await Responder.results.show_results(user_id, user_data)

    # handle RESULTS response
    if stage == "results":
        return await results_callback(update, context, video_auto_callback)

    # finish order creation
    if stage == "results_confirmed":
        await add_order_to_db(user_id, user_data)
        print("Added this order:")
        pprint(user_data)
        user_data.clear()
        return await Responder.results.results_correct(user_id)
