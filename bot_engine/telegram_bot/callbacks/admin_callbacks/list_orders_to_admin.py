import time
from datetime import datetime

from config import BOT_ADMIN
from container_interaction.helpers import UserPermission
from container_interaction.orders_db import fetch_orders
from container_interaction.users_db import get_user_data
from telegram_bot.responders.main_responder import Responder


async def list_10_orders_to_admin() -> None:
    all_orders = await fetch_orders()
    print(f"{all_orders=}")
    if not all_orders:
        return await Responder.admin_panel.missing_orders(BOT_ADMIN)

    sorted_orders_list = sorted(all_orders, key=lambda d: d["id"], reverse=True)
    last_ten_orders = sorted_orders_list[-10:]

    for order in last_ten_orders:
        order_time_iso = order.get("order_creation_end_timestamp")
        wait_time = datetime.now() - datetime.fromisoformat(order_time_iso).replace(
            tzinfo=None
        )
        order.update({"wait_time": str(wait_time).split(".")[0]})
        await Responder.admin_panel.list_single_order(
            BOT_ADMIN,
            order,
        )

    return True


async def list_active_orders_to_admin() -> None:
    active_orders = await fetch_orders("active")
    print(f"{active_orders=}")
    if not active_orders:
        return await Responder.admin_panel.missing_orders(BOT_ADMIN)

    for order in active_orders:
        order_time_iso = order.get("order_creation_end_timestamp")
        wait_time = datetime.now() - datetime.fromisoformat(order_time_iso).replace(
            tzinfo=None
        )
        order.update({"wait_time": str(wait_time).split(".")[0]})
        await Responder.admin_panel.list_single_order(
            BOT_ADMIN,
            order,
        )
    return True
