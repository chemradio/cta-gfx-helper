import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import config
from config import REQUEST_TYPE_TEMP_MAP
from telegram_bot.bot_instance import bot


class ResultsResponder:
    @staticmethod
    async def results_correct(user_id: int):
        return await bot.send_message(
            chat_id=user_id,
            text="✅ Заказ принят, ожидай. Или начни следющий - /start",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def results_incorrect(user_id: int):
        return await bot.send_message(
            chat_id=user_id,
            text="❌ Заказ отменен. Начать новый - /start",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def show_results(user_id: int, user_data: dict):
        """Prompt user the results."""
        results_message = str("РЕЗУЛЬТАТЫ:\n\n")
        request_type = REQUEST_TYPE_TEMP_MAP[user_data.get("request_type")]
        results_message += f"🍱 Тип заказа: {request_type}\n"

        if request_type == "readtime":
            readtime_text = user_data.get("readtime_text")
            readtime_speed = user_data.get("readtime_text")
            readtime_result = user_data.get("readtime_result")
            results_message += f"{readtime_text} {readtime_speed} {readtime_result}"
            return await bot.send_message(
                chat_id=user_id,
                text=results_message,
                reply_markup=ReplyKeyboardRemove(),
                parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
                disable_web_page_preview=True,
            )

        results_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Да", callback_data="results_correct"),
                    InlineKeyboardButton(f"Нет", callback_data="results_incorrect"),
                ]
            ]
        )

        temp_map = {
            True: "Да",
            False: "Нет",
        }

        link = user_data.get("screenshot_link")
        quote_text: str = user_data.get("quote_text")
        quote_author_text: str = user_data.get("quote_author_text")
        audio_enabled: bool = user_data.get("audio_enabled")

        if link:
            results_message += f"🔗 Ссылка: {link}\n"

        if quote_text:
            results_message += f"📜 Текст цитаты: {html.escape(quote_text)}\n"

        if quote_author_text:
            results_message += f"📜 Автор цитаты: {html.escape(quote_author_text)}\n"

        if audio_enabled:
            results_message += f"🔊 Аудио-файл: {temp_map[audio_enabled]}\n"

        user_data.update({"results_message": results_message})
        return await bot.send_message(
            chat_id=user_id,
            text=results_message,
            reply_markup=results_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
            disable_web_page_preview=True,
        )
