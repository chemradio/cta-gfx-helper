from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class AudioResponder:
    @staticmethod
    async def ask_audio_enabled(user_id):
        """Ask user if he needs a QUOTE-BOX."""
        quote_enabled_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Да", callback_data="audio_enabled"),
                    InlineKeyboardButton(f"Нет", callback_data="audio_disabled"),
                ]
            ]
        )

        await bot.send_message(
            chat_id=user_id,
            text="🔊 Аудио-файл:",
            reply_markup=quote_enabled_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_send_audio(user_id) -> None:
        await bot.send_message(
            chat_id=user_id,
            text="🔊 Пришли мне аудио-файл в формате MP3 или WAV. Не длиннее 30 секунд.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
