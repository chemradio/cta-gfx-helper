import time
import datetime
import interlinks
import engines.utils
from engines.telegram_bot.bot_instance import bot
from database.db import db_handler
from telegram import (
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
)
from telegram.ext import CallbackContext

def only_admin(func):
    def wrapper(*args, **kwargs):
        if args[0].message.from_user.id in interlinks.ADMIN_TELEGRAM_IDS:
            return func(*args, **kwargs)
        else:
            return False
    return wrapper


@only_admin
def register_requests_handler(update: Update, _: CallbackContext) -> None:
    pending_register_requests = db_handler.get_pending_register_requests()
    if pending_register_requests:
        for index, request in enumerate(pending_register_requests, start=1):
            keyboard = [
                [
                    InlineKeyboardButton(
                        f"Approve {request['first_name']}",
                        callback_data=f'approve {request["telegram_id"]}',
                    ),
                    InlineKeyboardButton(
                        f"Decline {request['first_name']}",
                        callback_data=f'block {request["telegram_id"]}',
                    ),
                ]
            ]

            approve_decline_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=interlinks.ADMIN_TELEGRAM_IDS[0],
                text=f'Pending request {index}:\n\nFirst Name: {request["first_name"]}\nTelegram ID: {request["telegram_id"]}',
                reply_markup=approve_decline_markup,
            )

    else:
        bot.send_message(
            chat_id=interlinks.ADMIN_TELEGRAM_IDS[0],
            text=f"No pending register requests",
            reply_markup=ReplyKeyboardRemove(),
        )
    return


@only_admin
def registered_users_handler(update: Update, _: CallbackContext) -> None:
    registered_users = db_handler.get_registered_users()
    if registered_users:
        for index, user in enumerate(registered_users, start=1):
            keyboard = [
                [
                    InlineKeyboardButton(
                        f"Block {user['first_name']}",
                        callback_data=f'block {user["telegram_id"]}',
                    )
                ]
            ]

            remove_button_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=interlinks.ADMIN_TELEGRAM_IDS[0],
                text=f"Registered user {index}:\n\nFirst Name: {user['first_name']}\nTelegram ID: {user['telegram_id']}",
                reply_markup=remove_button_markup,
            )
    else:
        bot.send_message(
            chat_id=interlinks.ADMIN_TELEGRAM_IDS[0],
            text=f"No registered users",
            reply_markup=ReplyKeyboardRemove(),
        )
    return


@only_admin
def blocked_users_handler(update: Update, _: CallbackContext) -> None:
    blocked_users = db_handler.get_blocked_users()
    if blocked_users:
        for index, user in enumerate(blocked_users, start=1):
            keyboard = [
                [
                    InlineKeyboardButton(
                        f"Approve {user['first_name']}",
                        callback_data=f'approve {user["telegram_id"]}',
                    )
                ]
            ]

            approve_button_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=interlinks.ADMIN_TELEGRAM_IDS[0],
                text=f"Blocked user {index}:\n\nFirst Name: {user['first_name']}\nTelegram ID: {user['telegram_id']}",
                reply_markup=approve_button_markup,
            )
    else:
        bot.send_message(
            chat_id=interlinks.ADMIN_TELEGRAM_IDS[0],
            text=f"No blocked users",
            reply_markup=ReplyKeyboardRemove(),
        )
    return


@only_admin
def recent_orders(update: Update, _: CallbackContext) -> None:
    results = db_handler.get_recent_orders()
    if results:
        for index, result in enumerate(results, start=1):
            order = dict(result)
            message_string = f"<b>Order #{index}, docID: {result.doc_id}</b>\n\n"
            for key, value in order.items():
                message_string += f"{key}: {value}\n"

            bot.send_message(
                update.message.from_user.id,
                message_string,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
    return


@only_admin
def processing_orders(update: Update, _: CallbackContext) -> None:
    processing_orders_list = db_handler.get_processing_orders()
    if processing_orders_list:
        for index, order in enumerate(processing_orders_list, start=1):
            terminate_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"Terminate Order",
                            callback_data=f"terminate_order {order.doc_id}",
                        )
                    ]
                ]
            )
            order_dict = dict(order)
            message_string = f"<b>Order #{index}, docID: {order.doc_id}</b>\n"
            message_string += f'Processing time: {str(datetime.timedelta(seconds=int(time.time() - order["start_render_timestamp"])))}\n\n'
            for key, value in order_dict.items():
                message_string += f"{key}: {value}\n"
            bot.send_message(
                interlinks.ADMIN_TELEGRAM_IDS[0],
                message_string,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=terminate_markup,
            )

    else:
        bot.send_message(interlinks.ADMIN_TELEGRAM_IDS[0], "No active processing orders")
    return


@only_admin
def active_orders(update: Update, _: CallbackContext) -> None:
    active_orders = db_handler.get_active_orders()
    if active_orders:
        for index, result in enumerate(active_orders, start=1):
            terminate_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"Terminate Order",
                            callback_data=f"terminate_order {result.doc_id}",
                        )
                    ]
                ]
            )
            order = dict(result)
            message_string = f"<b>Order #{index}, docID: {result.doc_id}</b>\n\n"

            for key, value in order.items():
                message_string += f"{key}: {value}\n"

            bot.send_message(
                update.message.from_user.id,
                message_string,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=terminate_markup,
            )
    else:
        bot.send_message(update.message.from_user.id, "No currently active orders")
    return


@only_admin
def terminate_sessions(update: Update, _: CallbackContext) -> None:
    if db_handler.start_terminate_all_active_sessions():
        bot.send_message(interlinks.ADMIN_TELEGRAM_IDS[0], "All sessions terminated")
    else:
        bot.send_message(interlinks.ADMIN_TELEGRAM_IDS[0], "No active sessions")
    return





@only_admin
def clear_bot_cache(update: Update, _: CallbackContext) -> None:
    active_orders = db_handler.get_active_orders()
    if active_orders:
        update.message.reply_text(
            "There are /active_orders. /terminate_sessions to proceed."
        )
        return
    else:
        engines.utils.clear_assets_folder()
        update.message.reply_text("Cache cleared.")
    return


@only_admin
def cache_size(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        f"Cache size:\n<b>{engines.utils.get_cache_size()} MB</b>\n\n/clear_bot_cache",
        parse_mode=ParseMode.HTML,
    )


@only_admin
def send_announcement(update: Update, _: CallbackContext) -> None:
    # notify_end_previous_sessions(user_id=update.message.from_user.id, chat_id=update.message.chat.id)
    db_handler.terminate_all_sessions(update.message.from_user.id)
    db_handler.add_db_entry({
        "status": 'active',
        'request_type': 'send_announcement',
        "first_name": update.message.from_user.first_name,
        "telegram_id": update.message.from_user.id,
        "start_timestamp": update.message.date.timestamp(),
        'stage': 'awaiting_announcement'
    })

    update.message.reply_text('Пришли текст для рассылки зарегистрированным пользователям.')
    return
