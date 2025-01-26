from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class VideoFilesResponder:
    @staticmethod
    async def ask_main_file(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="🎨 Пришли основной файл для графики (JPEG / PNG / PDF / WORD).",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_background_source(user_id):
        bg_source_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"Скриншот", callback_data="background_screenshot"
                    ),
                    InlineKeyboardButton(f"Есть файл", callback_data="background_file"),
                    InlineKeyboardButton(
                        f"Без подложки", callback_data="no_background"
                    ),
                ]
            ]
        )

        await bot.send_message(
            chat_id=user_id,
            text="""🎨 Подложка: у тебя есть файл или сделать скриншот с сайта?
        
Графика без подложки делается только из высококачественного скриншота с веб-сайта. Не выбирай БЕЗ ПОДЛОЖКИ, если не уверен в этом абсолютно.""",
            reply_markup=bg_source_keyboard,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_background_file(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="🎨 Пришли мне файл для подложки (JPEG / PNG / PDF).",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_background_link(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="🔗 Пришли мне ссылку для подложки.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
