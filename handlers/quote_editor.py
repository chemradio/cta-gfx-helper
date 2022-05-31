from interlinks import delegate_editor as editor_id
from engines.telegram_bot import bot

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
)

from engines.telegram_bot import bot
from tinydb.table import Document
from database.db import db_handler


def check_quote(db_query: Document):
    db_handler.update_doc_db_parameters(
        doc_id=db_query.doc_id,
        parameters={
            "chat_id": db_query["telegram_id"],
            "stage": "check_quote",
            "qc_quote_checked": False,
            "qc_main_notification_sent": False,
            "qc_quote_text_sent": False,
            "qc_quote_text_received": False,
            "qc_quote_author_sent": False,
            "qc_quote_author_received": False,
            "qc_final_confirmed": False,
        },
    )

    # start thread

    check_quote_message = f""" Новый заказ на графику с цитатой:
Номер заказа: {db_query.doc_id}

Автор цитаты: {db_query['quote_author'] if db_query['quote_author_enabled'] else 'НЕ УКАЗАН'}

Текст Цитаты: {db_query['quote_text']}"""

    quote_check_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"Все ОК!", callback_data=f"quote_check_ok_{db_query.doc_id}"
                ),
                InlineKeyboardButton(
                    f"Исправить", callback_data=f"quote_check_edit_{db_query.doc_id}"
                ),
            ]
        ]
    )

    bot.send_message(
        chat_id=editor_id,
        text=check_quote_message,
        reply_markup=quote_check_markup,
        # parse_mode=ParseMode.HTML, - gives errors if tags in quote text...
    )

    return
