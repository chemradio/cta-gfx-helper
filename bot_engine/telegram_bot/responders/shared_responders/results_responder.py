import config
from telegram_bot.responders.bot_texts import Responses
from telegram_bot.bot_instance import bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from config import REQUEST_TYPE_TEMP_MAP


class ResultsResponder:
    @staticmethod
    async def results_correct(user_id: int):
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.results.results_correct,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def results_incorrect(user_id: int):
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.results.results_incorrect,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def show_results(user_id: int, user_data: dict):
        """Prompt user the results."""
        results_message = str("РЕЗУЛЬТАТЫ:\n\n")
        request_type = REQUEST_TYPE_TEMP_MAP[user_data.get("request_type")]
        results_message += f"{Responses.results.request_type}: {request_type}\n\n"

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

        link = user_data.get("link")
        bg_animation: str = user_data.get("bg_animation")
        fg_enabled: bool = user_data.get("fg_enabled")
        fg_animation: str = user_data.get("fg_animation")
        quote_enabled: bool = user_data.get("quote_enabled")
        quote_text: str = user_data.get("quote_text")
        quote_author_enabled: bool = user_data.get("quote_author_enabled")
        quote_author_text: str = user_data.get("quote_author_text")
        audio_enabled: bool = user_data.get("audio_enabled")

        if link:
            results_message += f"{Responses.results.link} {link}\n\n"
        if bg_animation:
            results_message += (
                f"{Responses.results.bg_animation} {bg_animation.capitalize()}\n"
            )
        if fg_enabled:
            results_message += (
                f"{Responses.results.fg_animation} {fg_animation.capitalize()}\n\n"
            )

        if quote_enabled:
            results_message += f"{Responses.results.quote_text} {quote_text}\n"

        if quote_author_enabled:
            results_message += (
                f"{Responses.results.quote_author_text} {quote_author_text}\n\n"
            )

        if audio_enabled:
            results_message += (
                f"{Responses.results.audio_enabled} {temp_map[audio_enabled]}\n"
            )

        user_data.update({"results_message": results_message})
        return await bot.send_message(
            chat_id=user_id,
            text=results_message,
            reply_markup=results_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
            disable_web_page_preview=True,
        )
