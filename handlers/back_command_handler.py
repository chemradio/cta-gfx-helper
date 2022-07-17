from engines.telegram_bot.bot_instance import bot

from database.db import db_handler
from telegram import (
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    CallbackContext,
)


from handlers.decorators import log_decorator
from handlers.error_responses import no_active_session_notification
from handlers.question_senders import (
    ask_for_link,
    ask_quote_enabled,
    ask_bg_animation_type,
    ask_audio_enabled,
    ask_fg_enabled,
)


@log_decorator
def back_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    db_id = db_handler.get_active_doc_id(user_id)
    if not db_id:  # check if the session expired first
        no_active_session_notification(user_id)
        return

    current_stage = db_handler.get_current_stage(user_id)
    request_type = db_handler.get_request_type(user_id)

    if request_type == "only_screenshots":
        db_handler.terminate_all_sessions(user_id)
        bot.send_message(
            chat_id=user_id,
            text="Заказ отменен. Можешь оформить новый через /start.",
            reply_markup=ReplyKeyboardRemove(),
        )

    elif request_type == "video_auto":
        if current_stage == "link":
            db_handler.terminate_all_sessions(user_id)
            bot.send_message(
                chat_id=user_id,
                text="Заказ отменен. Можешь оформить новый через /start.",
                reply_markup=ReplyKeyboardRemove(),
            )

        elif current_stage == "quote_enabled":
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"stage": "link", "link": ""}
            )
            ask_for_link(user_id)

        elif (
            current_stage == "quote_text"
            or "quote_author_enabled"
            or "quote_author_text"
            or "audio_enabled"
        ):
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "stage": "quote_enabled",
                    "quote_enabled": False,
                    "quote_text": "",
                    "quote_author_enabled": False,
                    "quote_author_text": "",
                },
            )
            ask_quote_enabled(user_id)

        elif current_stage == "send_audio" or "check":
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "stage": "audio_enabled",
                    "audio_enabled": False,
                    "audio_path": "",
                },
            )
            ask_audio_enabled(user_id)

    elif request_type == "video_files":
        if current_stage == "bg_animation_type":
            db_handler.terminate_all_sessions(user_id)
            bot.send_message(
                chat_id=user_id,
                text="Заказ отменен. Можешь оформить новый через /start.",
                reply_markup=ReplyKeyboardRemove(),
            )

        elif current_stage == "send_bg" or "fg_enabled":
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "stage": "bg_animation_type",
                    "bg_animation_type": "",
                    "bg_path": "",
                },
            )
            ask_bg_animation_type(user_id)

        elif current_stage == "send_fg" or "fg_animation_type" or "quote_enabled":
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "stage": "fg_enabled",
                    "fg_enabled": False,
                    "is_two_layer": False,
                    "fg_path": "",
                    "fg_animation_type": "",
                },
            )
            ask_fg_enabled(user_id)

        elif (
            current_stage == "quote_text"
            or "quote_author_enabled"
            or "quote_author_text"
            or "audio_enabled"
        ):
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "stage": "quote_enabled",
                    "quote_enabled": False,
                    "quote_text": "",
                    "quote_author_enabled": False,
                    "quote_author_text": "",
                },
            )
            ask_quote_enabled(user_id)

        elif current_stage == "send_audio" or "check":
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "stage": "audio_enabled",
                    "audio_enabled": False,
                    "audio_path": "",
                },
            )
            ask_audio_enabled(user_id)

    else:
        pass
