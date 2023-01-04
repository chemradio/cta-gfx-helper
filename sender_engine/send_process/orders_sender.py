import asyncio
import threading
import time

from bot_instance import bot
from config import BOT_ADMIN
from container_interaction.edit_order_db import mark_order_sent
from container_interaction.gather_orders import get_ready_to_send_order
from send_process.send_order import send_order


async def orders_sender():
    while True:
        order = get_ready_to_send_order()
        if not order:
            break

        sent_order = await send_order(order)

        if not sent_order.get("send_success"):
            await bot.send_message(BOT_ADMIN, f"Failed to send order\n\n{order}")

        mark_success = await mark_order_sent(sent_order)

        if not mark_success:
            await bot.send_message(
                BOT_ADMIN,
                f"Failed to mark sent order\n{sent_order.get('send_success')=}\n\n{sent_order=}",
            )

        time.sleep(3)

    return True


def orders_sender_thread():
    thread_name = "orders_sender"
    for thread in threading.enumerate():
        if thread_name in thread.name:
            print(f"Thread {thread_name} already running... Returning")
            return

    threading.Thread(
        target=asyncio.run,
        args=(orders_sender(),),
        name=thread_name,
    ).start()
