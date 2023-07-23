from container_interaction.screenshoter import signal_to_screenshoter
from container_interaction.sender import signal_to_sender
from container_interaction.video_gfx import signal_to_video_gfx
from db_tortoise.orders_models import Order


def signal_to_services(order: Order):
    match order.current_stage:
        case "ready_for_screenshots":
            return signal_to_screenshoter()
        case "ready_for_video_gfx":
            return signal_to_video_gfx()
        case "ready_for_send":
            return signal_to_sender(order)
        case _:
            pass
