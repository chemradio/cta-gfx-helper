import time
from config import BOT_ADMIN
from py_gfxhelper_lib.order_enums import OrderStatus
from container_interaction.orders import fetch_orders

from telegram_bot.responders.main_responder import Responder


async def list_10_orders_to_admin() -> None:
    all_orders = await fetch_orders()
    if not all_orders:
        return await Responder.admin_panel.missing_orders(BOT_ADMIN)

    for order in all_orders[:10]:
        add_wait_time_to_order(order)
        return await Responder.admin_panel.list_single_order(
            BOT_ADMIN,
            order,
        )


async def list_active_orders_to_admin() -> None:
    active_orders = await fetch_orders(status=OrderStatus.PROCESSING)
    if not active_orders:
        return await Responder.admin_panel.missing_orders(BOT_ADMIN)

    for order in active_orders:
        add_wait_time_to_order(order)
        return await Responder.admin_panel.list_single_order(
            BOT_ADMIN,
            order,
        )


def add_wait_time_to_order(order: dict) -> None:
    order_created = int(order.get("created"))
    order.update({"wait_time": format_seconds(time.time() - order_created)})


def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
