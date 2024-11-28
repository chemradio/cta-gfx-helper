from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot.bot_instance import bot
import config


class OnlyScreenshotsResponder:
    @staticmethod
    async def results(user_id, context: ContextTypes.DEFAULT_TYPE):
        results = (
            f"Заказ на скриншоты из этой ссылки:\n\n{context.user_data.get('link')}"
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
