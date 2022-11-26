import config
from telegram_bot.responders.bot_texts import Responses
from telegram_bot.bot_instance import bot
from telegram import ReplyKeyboardRemove


class LinkResponder:
    @staticmethod
    async def ask_link(user_id) -> None:
        await bot.send_message(
            chat_id=user_id,
            text=Responses.link.link,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def bad_link(user_id) -> None:
        await bot.send_message(
            chat_id=user_id,
            text=Responses.link.bad_link,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
