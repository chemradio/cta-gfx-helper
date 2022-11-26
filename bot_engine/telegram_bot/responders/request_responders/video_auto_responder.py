from telegram_bot.bot_instance import bot
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import config
import inspect


class VideoAutoResponder:
    @staticmethod
    async def video_auto_results(user_id, context: ContextTypes.DEFAULT_TYPE):
        results = inspect.cleandoc(
            f"""\
            Заказ на графику из файлов

            Ссылка:
            {context.user_data.get('link', 'Отсутствует')}
           
            Текст цитаты:
            {context.user_data.get('quote_text', 'Отсутствует')}

            Автор цитаты:
            {context.user_data.get('quote_author_text', 'Отсутствует')}

            Аудио:
            {context.user_data.get('audio_enabled', 'Отсутствует')}
        """
        )

        results_correct_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Все верно", callback_data="results_correct"),
                    InlineKeyboardButton(
                        f"Отменить заказ", callback_data="results_incorrect"
                    ),
                ]
            ]
        )

        await bot.send_message(
            chat_id=user_id,
            text=results,
            reply_markup=results_correct_keyboard,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
