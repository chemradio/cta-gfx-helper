from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import config
from telegram_bot.bot_instance import bot


class StartResponder:
    @staticmethod
    async def ask_order_type(user_id):
        order_type_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Графика из ссылки", callback_data="video_auto"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Графика из файлов",
                        callback_data="video_files",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Только скриншоты",
                        callback_data="only_screenshots",
                    ),
                ],
                [
                    InlineKeyboardButton("Хрон текста", callback_data="readtime"),
                ],
            ]
        )

        await bot.send_message(
            chat_id=user_id,
            text="🍱 Выбери тип заказа",
            reply_markup=order_type_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
