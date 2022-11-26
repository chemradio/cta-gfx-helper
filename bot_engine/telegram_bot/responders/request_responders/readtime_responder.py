import config
from telegram_bot.responders.bot_texts import Responses
from telegram_bot.bot_instance import bot
from telegram import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


class ReadtimeResponder:
    @staticmethod
    async def ask_readtime_text(user_id):
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.readtime.send_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def bad_text(user_id):
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.readtime.bad_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_readtime_speed(user_id):
        readtime_speed_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Медленно", callback_data="slow_readtime"),
                    InlineKeyboardButton(f"Средне", callback_data="medium_readtime"),
                    InlineKeyboardButton(f"Быстро", callback_data="fast_readtime"),
                ]
            ]
        )
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.readtime.set_speed,
            reply_markup=readtime_speed_keyboard,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def readtime_results(user_id, context):
        user_data = context.user_data
        speed = user_data["readtime_speed"]
        readtime = user_data["readtime_result"]
        results_text = Responses.readtime.results.format(speed=speed, readtime=readtime)

        return await bot.send_message(
            chat_id=user_id,
            text=results_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
