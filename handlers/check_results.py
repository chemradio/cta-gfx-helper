from engines.telegram_bot.bot_instance import bot

from database.db import db_handler
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
)

from handlers.decorators import log_decorator
from handlers.error_responses import gp_error_notification


@log_decorator
def check_results(user_id):
    query = db_handler.get_active_entry_data(user_id)
    if query:
        if query["request_type"] == "only_screenshots":
            user_results = f"<b><u>РЕЗУЛЬТАТЫ:</u></b>\n\nБуду делать скриншоты из этой ссылки:\n\n{query['link']}"

        elif query["request_type"] == "video_auto":
            user_results = (
                f"<b><u>РЕЗУЛЬТАТЫ:</u></b>\n\n<b>Ссылка:</b> {query['link']}\n_____\n"
            )
            if query["quote_enabled"]:
                user_results += (
                    f"<b>Цитата:</b> Да\n\n<b>Текст цитаты:</b> {query['quote_text']}"
                )
                if query["quote_author_enabled"]:
                    user_results += (
                        f"\n<b>Автор цитаты:</b> {query['quote_author']}\n_____"
                    )
                else:
                    user_results += "\n_____"
            if query["audio_enabled"]:
                user_results += f"\n<b>Аудио:</b> Да\n"

        elif query["request_type"] == "video_files":
            user_results = f'<b><u>РЕЗУЛЬТАТЫ:</u></b>\n\n<b>Анимация заднего фона:</b> {query["bg_animation_type"]}\n_____\n'
            if query["fg_enabled"]:
                user_results += f"<b>Анимация переднего плана:</b> {query['fg_animation_type']}\n_____\n"

            if query["quote_enabled"]:
                user_results += (
                    f"<b>Цитата:</b> Да\n\n<b>Текст цитаты:</b> {query['quote_text']}"
                )
                if query["quote_author_enabled"]:
                    user_results += (
                        f"\n<b>Автор цитаты:</b> {query['quote_author']}\n_____"
                    )
                else:
                    user_results += "\n_____"
            if query["audio_enabled"]:
                user_results += f"\n<b>Аудио:</b> Да\n"

        results_correct_incorrect_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"Все верно!", callback_data="results_correct"
                    ),
                    InlineKeyboardButton(
                        f"Нет, не верно", callback_data="results_incorrect"
                    ),
                ]
            ]
        )
        results_message_id = bot.send_message(
            chat_id=user_id,
            text=user_results,
            reply_markup=results_correct_incorrect_markup,
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML,
        ).message_id
        db_handler.update_db_parameters(
            user_id=user_id, parameters={"results_message_id": results_message_id}
        )
        return

    else:
        gp_error_notification(user_id=user_id)
        return
