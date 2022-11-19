from interlinks import stage_texts
from engines.telegram_bot.bot_instance import bot

from telegram import (
    ReplyKeyboardRemove,
    ParseMode,
)

from engines.telegram_bot.legacy_handlers.decorators import log_decorator



#### ERRORS ####
################################################################
@log_decorator
def wrong_link_notification(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["wrong_link"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def gp_error_notification(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["error"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def try_again_error(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["try_again"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def no_active_session_notification(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["no_active_session"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def wrong_audio_format(user_id):
    bot.send_message(
        chat_id=user_id,
        text="Прости, бот поддерживает звук только в форматаъ MP3 и WAV. Пожалуйста, используй один из этих форматов.",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def audio_length_exceeded(user_id):
    bot.send_message(
        chat_id=user_id,
        text="Аудио не может быть дольше <b>30 секунд</b>.\n\n<i>Пришли аудио покороче.</i>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )