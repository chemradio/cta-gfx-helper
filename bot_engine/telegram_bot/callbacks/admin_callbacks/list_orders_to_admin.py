import time

from config import BOT_ADMIN
from container_interaction.helpers import UserStatus
from container_interaction.orders_db import fetch_orders
from telegram_bot.responders.main_responder import Responder


async def list_10_orders_to_admin() -> None:
    all_orders = await fetch_orders()
    if not all_orders:
        return await Responder.admin_panel.missing_orders(BOT_ADMIN)

    sorted_orders_list = sorted(all_orders, key=lambda d: d["order_id"], reverse=True)
    last_ten_orders = sorted_orders_list[-10:]

    for order in last_ten_orders:
        wait_secs = time.time() - order.get("order_creation_end_timestamp")
        wait_time = time.strftime("%H:%M:%S", time.gmtime(wait_secs))
        order.update({"wait_time": wait_time})
        await Responder.admin_panel.list_single_order(BOT_ADMIN, order)

    return True


async def list_active_orders_to_admin() -> None:
    active_orders = await fetch_orders("active")
    if not active_orders:
        return await Responder.admin_panel.missing_orders(BOT_ADMIN)

    for order in active_orders:
        wait_secs = time.time() - order.get("order_creation_end_timestamp")
        wait_time = time.strftime("%H:%M:%S", time.gmtime(wait_secs))
        order.update({"wait_time": wait_time})
        await Responder.admin_panel.list_single_order(BOT_ADMIN, order)

    return True
