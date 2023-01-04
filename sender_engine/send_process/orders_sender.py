import asyncio
import threading
import time

from bot_instance import bot
from config import BOT_ADMIN
from container_interaction.edit_order_db import mark_order_sent
from container_interaction.gather_orders import get_ready_to_send_order
from send_process.send_order import send_order


def orders_sender():
    while True:

        print("enter orders sender")
        print("getting one order")

        order = get_ready_to_send_order()
        if not order:
            break

        print(f"order is ok, {order=}")

        sent_order = asyncio.run(send_order(order))
        print(f"{sent_order=}")
        if not sent_order.get("send_success"):
            asyncio.run(bot.send_message(BOT_ADMIN, f"Failed to send order\n\n{order}"))

        mark_success = mark_order_sent(sent_order)
        print(f"{mark_success=}")

        if not mark_success:
            asyncio.run(
                bot.send_message(
                    BOT_ADMIN,
                    f"Failed to mark sent order\n{sent_order.get('send_success')=}\n\n{sent_order=}",
                )
            )

        time.sleep(3)

    return True


def orders_sender_thread():
    thread_name = "orders_sender"
    for thread in threading.enumerate():
        if thread_name in thread.name:
            print(f"Thread {thread_name} already running... Returning")
            return

    thread = threading.Thread(
        target=orders_sender,
        name=thread_name,
    ).start()
    thread
