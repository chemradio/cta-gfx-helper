from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot
from telegram_bot.responders.bot_texts import Responses


class AdminPanelResponder:
    @staticmethod
    async def admin_panel(admin_id):
        admin_panel_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        Responses.admin.list_10_orders,
                        callback_data=f"admin_list_10_orders",
                    )
                ],
                [
                    InlineKeyboardButton(
                        Responses.admin.list_active_orders,
                        callback_data=f"admin_list_active_orders",
                    )
                ],
                [
                    InlineKeyboardButton(
                        Responses.admin.list_approved_users,
                        callback_data=f"admin_list_approved_users",
                    )
                ],
                [
                    InlineKeyboardButton(
                        Responses.admin.list_blocked_users,
                        callback_data=f"admin_list_blocked_users",
                    )
                ],
                [
                    InlineKeyboardButton(
                        Responses.admin.list_pending_users,
                        callback_data=f"admin_list_pending_users",
                    )
                ],
            ]
        )

        return await bot.send_message(
            chat_id=admin_id,
            text=Responses.admin.admin_panel,
            reply_markup=admin_panel_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def list_single_order(admin_id, order: dict):
        order_cancel_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        Responses.admin.cancel_order,
                        callback_data=f"admin_cancel_order_{order['order_id']}",
                    )
                ],
            ]
        )

        message_text = Responses.admin.list_single_order.format(
            order_id=order.get("order_id"),
            customer_name=order.get("user_first_name"),
            request_type=order.get("request_type"),
            status=order.get("status"),
            wait_time=order.get("wait_time"),
            link=order.get("link"),
            quote_text=order.get("quote_text"),
            quote_author=order.get("quote_author_text"),
            audio_enabled="Да" if order.get("audio_enabled") else "Нет",
        )

        return await bot.send_message(
            chat_id=admin_id,
            text=message_text,
            reply_markup=order_cancel_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
            disable_web_page_preview=True,
        )
