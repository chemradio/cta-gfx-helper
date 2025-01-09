from telegram import Update
from telegram.ext import ContextTypes

from container_interaction.orders import send_order_to_dispatcher
from .attachment_callbacks.attachment_handler import attachment_downloader
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from .shared_callbacks import results_callback, quote_callback, audio_callback
from telegram_bot.exceptions.attachments import AttachmentTypeMismatch, AttachmentNotFound, AttachmentNotNeeded, AttachmentSizeExceeded
from telegram_bot.responders.main_responder import Responder
from py_gfxhelper_lib.miscellaneous.check_url import check_is_url



async def video_files_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    # ask main file
    if stage == "start_order":
        user_data.update({"stage": "main_file"})
        return await Responder.video_files.ask_main_file(user_id)

    # handle main file
    # choose background file vs background screenshot
    if stage == "main_file":
        downloaded_file = await attachment_downloader(update, context)
        user_data.update({"main_file": downloaded_file, "stage": "background_source"})
        return await Responder.video_files.ask_background_source(user_id)


    # handle background source choice
    if stage == "background_source":
        try:
            if update.callback_query.data not in (
                "background_screenshot",
                "background_file",
                "no_background",
            ):
                raise Exception()

            await update.callback_query.answer(cache_time=180)

            user_data.update({"background_source": update.callback_query.data})
            match update.callback_query.data:
                case "background_screenshot":
                    user_data.update(
                        {"stage": "background_link", "request_type": "video_mixed"}
                    )
                    return await Responder.video_files.ask_background_link(user_id)
                case "background_file":
                    user_data.update({"stage": "background_file"})
                    return await Responder.video_files.ask_background_file(user_id)
                case "no_background":
                    user_data.update({"stage": "quote_enabled"})
                    return await Responder.quote.ask_quote_enabled(user_id)

        except:
            return await Responder.errors.gp_error(user_id)

    # handle background link
    if stage in ("background_link", "background_file"):
        if stage == "background_link":
            link_list = check_is_url(update.message.text)
            if not link_list:
                return await Responder.link.bad_link(user_id)
            user_data.update({"background_link": link_list[0]})

        elif stage == "background_file":
            downloaded_file = await attachment_downloader(update, context)
            user_data.update({"background_file": downloaded_file})

        user_data.update({"stage": "quote_enabled"})
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
        user_data = format_video_files_user_data(user_data)
        await send_order_to_dispatcher(user_id, user_data)
        user_data.clear()
        return await Responder.results.results_correct(user_id)

    return await Responder.errors.gp_error(user_id)



def format_video_files_user_data(user_data: dict) -> dict:
    main_file = user_data.pop("main_file")
    match user_data.pop("background_source"):
        case "no_background":
            user_data["background_name"] = main_file
            user_data["background_screenshot"] = False
            user_data["is_two_layer"] = False
        case "background_file":
            user_data["foreground_name"] = main_file
            user_data["background_name"] = user_data.pop("background_file")
            user_data["background_screenshot"] = False
            user_data["is_two_layer"] = True
        case "background_screenshot":
            user_data["foreground_name"] = main_file
            user_data["background_screenshot"] = True
            user_data["is_two_layer"] = True

    return user_data
