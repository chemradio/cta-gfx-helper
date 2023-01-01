from pprint import pprint

from telegram import Update
from telegram.ext import ContextTypes

from container_interaction.orders_db import add_order_to_db
from telegram_bot.callbacks.attachment_callbacks.attachment_handler import (
    attachment_downloader,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.callbacks.shared_callbacks.audio_callback import audio_callback
from telegram_bot.callbacks.shared_callbacks.quote_callback import quote_callback
from telegram_bot.callbacks.shared_callbacks.results_callback import results_callback
from telegram_bot.responders.bot_texts import Responses
from telegram_bot.responders.main_responder import Responder


async def video_files_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    # ask bg animation
    if stage == "start_order":
        user_data.update({"stage": "bg_animation"})
        return await Responder.video_files.ask_bg_animation(user_id)

    # handle bg animation
    # ask bg file
    if stage == "bg_animation":
        try:
            if update.callback_query.data not in ["bg_scroll", "bg_zoom"]:
                raise Exception()

            await update.callback_query.answer(cache_time=180)
            await update.callback_query.edit_message_text(
                text=Responses.video_files.bg_animation_type_responded.format(
                    # "bg_scroll" becomes "Scroll" for ex...
                    bg_animation=update.callback_query.data[3:].capitalize()
                )
            )
            user_data.update(
                {"bg_animation": update.callback_query.data[3:], "stage": "bg_file"}
            )
            return await Responder.video_files.ask_bg_file(user_id)
        except:
            return await Responder.errors.gp_error(user_id)

    # handle bg file
    # ask fg enabled
    if stage == "bg_file":
        downloaded_file = await attachment_downloader(update, context)
        user_data.update({"background_name": downloaded_file, "stage": "fg_enabled"})
        return await Responder.video_files.ask_fg_enabled(user_id)

    # handle fg enabled
    # ask fg animation
    if stage == "fg_enabled":
        try:
            if update.callback_query.data not in ["fg_enabled", "fg_disabled"]:
                raise Exception()

            temp_map = {"fg_enabled": "Да", "fg_disabled": "Нет"}
            await update.callback_query.answer(cache_time=180)
            await update.callback_query.edit_message_text(
                text=f"{Responses.video_files.fg_enabled} {temp_map[update.callback_query.data]}"
            )

            if update.callback_query.data == "fg_enabled":
                user_data.update({"fg_enabled": True, "stage": "fg_animation"})
                return await Responder.video_files.ask_fg_animation(user_id)
            else:
                user_data.update({"fg_enabled": False, "stage": "quote_enabled"})
                return await Responder.quote.ask_quote_enabled(user_id)
        except:
            return await Responder.errors.gp_error(user_id)

    # handle fg animation
    # ask fg file
    if stage == "fg_animation":
        try:
            if update.callback_query.data not in ["fg_scroll", "fg_zoom"]:
                raise Exception()

            await update.callback_query.answer(cache_time=180)
            await update.callback_query.edit_message_text(
                text=Responses.video_files.fg_animation_type_responded.format(
                    # "bg_scroll" becomes "Scroll" for ex...
                    fg_animation=update.callback_query.data[3:].capitalize()
                )
            )
            user_data.update(
                {"fg_animation": update.callback_query.data[3:], "stage": "fg_file"}
            )
            return await Responder.video_files.ask_fg_file(user_id)
        except:
            return await Responder.errors.gp_error(user_id)

    # handle fg file
    # ask quote
    if stage == "fg_file":
        downloaded_file = await attachment_downloader(update, context)
        user_data.update({"foreground_name": downloaded_file, "stage": "quote_enabled"})
        return await Responder.quote.ask_quote_enabled(user_id)

    # handle QUOTE responses
    if stage in [
        "quote_enabled",
        "quote_text",
        "quote_author_enabled",
        "quote_author_text",
    ]:
        return await quote_callback(update, context, video_files_callback)

    # ask AUDIO
    if stage == "quote_passed":
        user_data.update({"stage": "audio_enabled"})
        return await Responder.audio.ask_audio_enabled(user_id)

    # handle AUDIO responses
    if stage in ["audio_enabled", "audio_file"]:
        return await audio_callback(update, context, video_files_callback)

    # ask RESULTS
    if stage == "audio_passed":
        user_data.update({"stage": "results"})
        return await Responder.results.show_results(user_id, user_data)

    # handle RESULTS response
    if stage == "results":
        return await results_callback(update, context, video_files_callback)

    # finish order creation
    if stage == "results_confirmed":
        await add_order_to_db(user_id, user_data)
        user_data.clear()
        return await Responder.results.results_correct(user_id)

    return await Responder.errors.gp_error(user_id)
