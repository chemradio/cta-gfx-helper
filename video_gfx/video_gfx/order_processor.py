import asyncio
import threading

from container_interation.edit_order_db import mark_order_video_gfx
from container_interation.gather_orders import get_ready_to_video_gfx_order

from video_gfx.process_one_order import create_video_gfx


async def process_video_gfx_orders():
    while True:
        print("fetching one order")
        order = get_ready_to_video_gfx_order()
        print(f"fetched order: {order}")

        if not order:
            break

        video_gfx_success, error = create_video_gfx(order)

        if video_gfx_success:
            order["video_gfx_ready"] = True
        else:
            order["error"] = True
            order["error_type"] = f"video_gfx_error: {error}"

        mark_order_video_gfx(order)


def video_gfx_thread():
    thread_name = "video_gfx_thread"
    for thread in threading.enumerate():
        if thread_name in thread.name:
            print(f"Thread {thread_name} already running... Returning")
            return

    threading.Thread(
        target=asyncio.run,
        args=(process_video_gfx_orders(),),
        name=thread_name,
    ).start()
