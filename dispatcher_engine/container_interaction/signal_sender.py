from container_interaction.screenshoter import signal_to_screenshoter
from container_interaction.sender import signal_to_sender
from container_interaction.video_gfx import signal_to_video_gfx
from db_mongo.models.orders import Order


async def signal_to_services(order: Order):
    print(f"signalling to services, current stage is {order.current_stage}")
    match order.current_stage:
        case "ready_for_screenshots":
            print("Signalling to screenshooter")
            return await signal_to_screenshoter()
        case "ready_for_video_gfx":
            print("Signalling to video_gfx")
            return await signal_to_video_gfx()
        case "ready_for_send":
            print("Signalling to sender")
            return await signal_to_sender()
        case _:
            print("no match. signal declined")
            pass
