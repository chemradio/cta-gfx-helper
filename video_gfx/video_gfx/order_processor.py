from container_interation.gather_orders import get_ready_to_video_gfx_order
from video_gfx.process_one_order import create_video_gfx
from container_interation.edit_order_db import mark_order_video_gfx


def process_video_gfx_orders():
    while True:
        order = get_ready_to_video_gfx_order()
        if not order:
            break

        video_gfx_processed_order = create_video_gfx(order)
        mark_order_video_gfx(video_gfx_processed_order)
