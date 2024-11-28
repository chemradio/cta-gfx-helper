from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class AdminPanelResponder:
    @staticmethod
    async def admin_panel(admin_id):
        admin_panel_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🧾 Последние 10 заказов",
                        callback_data=f"admin_list_10_orders",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏳ Активные заказы",
                        callback_data=f"admin_list_active_orders",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👍 Одобренные пользователи",
                        callback_data=f"admin_list_approved_users",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🛑 Заблокированные пользователи",
                        callback_data=f"admin_list_blocked_users",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❔ Ожидающие пользователи",
                        callback_data=f"admin_list_pending_users",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "dump user db",
                        callback_data=f"dump_users",
                    )
                ],
            ]
        )

        return await bot.send_message(
            chat_id=admin_id,
            text="⌘ Панель администратора",
            reply_markup=admin_panel_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def list_single_order(admin_id, order: dict):
        order_cancel_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🛑 Отменить заказ",
                        callback_data=f"admin_cancel_order_{order['id']}",
                    )
                ],
            ]
        )

        message_text = """Заказ № {order_id}

Статус: {status}

Заказчик: {customer_name}
Тип заказа: {request_type}
Cтатус: {status}
Время ожидания: {wait_time}

Ссылка: {link}
Цитата: {quote_text}
Автор цитаты: {quote_author}
Звук: {audio_enabled}""".format(
            order_id=order.get("id"),
            customer_name=order["user"].get("first_name"),
            customer_email=order["user"].get("email"),
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
            # text=dict(order),
            reply_markup=order_cancel_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
            disable_web_page_preview=True,
        )

    @staticmethod
    async def cookie_file_upload_status(admin_id, status: bool):
        if status is True:
            text = "Cookie-файл успешно загружен"
        else:
            text = "Ошибка загрузки cookie-файла"

        return await bot.send_message(
            chat_id=admin_id,
            text=text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
            disable_web_page_preview=True,
        )

    @staticmethod
    async def missing_orders(admin_id):
        return await bot.send_message(
            chat_id=admin_id,
            text="😶 Заказы с таким критерием отсутствуют.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
            disable_web_page_preview=True,
        )
