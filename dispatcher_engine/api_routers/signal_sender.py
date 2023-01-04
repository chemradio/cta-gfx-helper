from container_interation.screenshoter import signal_to_screenshoter
from container_interation.sender import signal_to_sender
from container_interation.video_gfx import signal_to_video_gfx


def signal_to_services(current_stage):
    match current_stage:
        case "ready_for_screenshots":
            return signal_to_screenshoter()
        case "ready_for_video_gfx":
            return signal_to_video_gfx()
        case "ready_for_send":
            return signal_to_sender()
        case _:
            pass
