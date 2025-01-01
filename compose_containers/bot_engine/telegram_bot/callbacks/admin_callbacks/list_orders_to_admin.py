import time
from datetime import datetime

from config import BOT_ADMIN
from telegram_bot.custom_types.user_permission_role import UserPermission
from container_interaction.orders import fetch_orders
from container_interaction.users import get_user_data
from telegram_bot.responders.main_responder import Responder


async def list_10_orders_to_admin() -> None:
    all_orders: list[dict] = await fetch_orders()

    if not all_orders:
        return await Responder.admin_panel.missing_orders(BOT_ADMIN)

    for order in all_orders:
        order_time_iso = order.get("order_creation_end_timestamp")

        wait_time = datetime.now() - datetime.fromisoformat(order_time_iso).replace(
            tzinfo=None
        )

        order.update({"wait_time": str(wait_time).split(".")[0]})
        try:
            await Responder.admin_panel.list_single_order(
                BOT_ADMIN,
                order,
            )
        except Exception as e:
            print(str(e), flush=True)

    return True


async def list_active_orders_to_admin() -> None:
    active_orders = await fetch_orders("active")
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
