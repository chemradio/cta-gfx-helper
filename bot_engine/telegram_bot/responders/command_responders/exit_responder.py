import config
from telegram_bot.responders.bot_texts import Responses
from telegram_bot.bot_instance import bot
from telegram import ReplyKeyboardRemove


class ExitResponder:
    @staticmethod
    async def exit_terminate_order(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.command.exit_message,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    async def exit_missing_order(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.command.exit_message_missing_orders,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
