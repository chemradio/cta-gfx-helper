import interlinks
import secrets

from pydub import AudioSegment
from PIL import Image
from database.db import db_handler
from telegram import (
    ReplyKeyboardRemove,
    Update,
    ParseMode,
)
from telegram.ext import (
    CallbackContext,
)

from handlers.error_responses import (
    no_active_session_notification,
    wrong_audio_format,
    audio_length_exceeded,
)

from handlers.check_results import (
    check_results,
)

from handlers.question_senders import (
    ask_fg_animation_type,
    ask_fg_enabled,
)


################################################################
# ATTACHMENT Handler
################################################################
def attachment_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_first_name = update.message.from_user.first_name
    save_file_name_start = (
        interlinks.user_files_folder + "/" + f"user_{secrets.token_hex(8)}"
    )
    current_stage = db_handler.get_current_stage(user_id=user_id)

    if not current_stage:
        no_active_session_notification(user_id)
        return

    # logger_bot.debug("Attachment handler", user_id, user_first_name, current_stage)

    if update.to_dict()["message"].get("reply_to_message"):
        message = update.message.reply_to_message
    else:
        message = update.message

    if current_stage == "send_audio":
        if message.audio:
            if message.audio.mime_type == "audio/mpeg3" or "audio/mpeg":
                extension = ".mp3"
            elif message.audio.mime_type == "audio/x-wav":
                extension = ".wav"

            else:
                wrong_audio_format(user_id)

            save_file_name = save_file_name_start + extension
            message.audio.get_file().download(custom_path=save_file_name, timeout=180)

            try:
                audio_file = AudioSegment.from_file(save_file_name, extension[1:])
                if audio_file.duration_seconds > 40:
                    audio_length_exceeded(user_id)
                    return
            except:
                ...

            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "audio_path": save_file_name,
                    "stage": "check",
                },
            )
            check_results(user_id=user_id)

        elif message.voice:
            save_file_name = save_file_name_start + ".ogg"
            message.voice.get_file().download(custom_path=save_file_name)
            ogg_audio = AudioSegment.from_ogg(save_file_name)
            ogg_audio.export(f"{save_file_name_start}.mp3", format="mp3")

            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "audio_path": f"{save_file_name_start}.mp3",
                    "stage": "check",
                },
            )
            check_results(user_id=user_id)
        else:
            wrong_audio_format(user_id)
            return

    elif current_stage == "send_bg" or current_stage == "send_fg":
        target_path = "bg_path" if current_stage == "send_bg" else "fg_path"

        if message.photo:
            photo_file_size = 0
            best_quality_photo_index = 0
            for index, photo in enumerate(message.photo):
                if photo["file_size"] > photo_file_size:
                    photo_file_size = photo["file_size"]
                    best_quality_photo_index = index

            save_file_name = save_file_name_start + ".png"
            message.photo[best_quality_photo_index].get_file().download(
                custom_path=save_file_name
            )

            with open(save_file_name, "rb") as im:
                Image.open(im).save(save_file_name, "PNG")

            db_handler.update_db_parameters(
                user_id=user_id, parameters={target_path: save_file_name}
            )

        elif message.document:
            if message.document.mime_type == "application/pdf":
                save_file_name = save_file_name_start + ".pdf"
                message.document.get_file().download(custom_path=save_file_name)

            elif "image" in message.document.mime_type:
                message.document.get_file().download(custom_path=save_file_name_start)
                save_file_name = save_file_name_start + ".png"
                with open(save_file_name_start, "rb") as im:
                    Image.open(im).save(save_file_name, "PNG")

            else:
                message.reply_text(
                    "Прости, бот поддерживает только PDF, PNG и JPG файлы. Пожалуйста, отправь изображение в одном из этих форматов.",
                    reply_markup=ReplyKeyboardRemove(),
                )
                return

        else:
            message.reply_text(
                "Прости, бот поддерживает только PDF, PNG и JPG файлы. Пожалуйста, отправь изображение в одном из этих форматов.",
                reply_markup=ReplyKeyboardRemove(),
            )
            return

        if current_stage == "send_bg":
            parameters = {
                "bg_path": save_file_name,
                "stage": "fg_enabled",
            }
            db_handler.update_db_parameters(user_id=user_id, parameters=parameters)
            ask_fg_enabled(user_id)

        elif current_stage == "send_fg":
            parameters = {
                "fg_path": save_file_name,
                "stage": "fg_animation_type",
            }
            db_handler.update_db_parameters(user_id=user_id, parameters=parameters)
            ask_fg_animation_type(user_id)

    else:
        message.reply_text(
            interlinks.stage_texts["unnecessary_file"], parse_mode=ParseMode.HTML
        )
