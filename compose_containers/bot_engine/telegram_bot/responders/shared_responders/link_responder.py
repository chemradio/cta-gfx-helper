from telegram import ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class LinkResponder:
    @staticmethod
    async def ask_link(user_id) -> None:
        await bot.send_message(
            chat_id=user_id,
            text="🔗 Пришли нужную ссылку.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def bad_link(user_id) -> None:
        await bot.send_message(
            chat_id=user_id,
            text="🆘🔗 Не могу обработать эту ссылку. Пожалуйста, пришли другую.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
