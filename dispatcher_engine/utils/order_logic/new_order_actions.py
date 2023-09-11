import secrets
from datetime import datetime

from db_mongo.models.orders import Order
from utils.helper_enums.orders import OrderRequestType


def assign_filenames(order: Order) -> None:
    background_name = f"01_BG_{secrets.token_hex(8)}.png"
    foreground_name = f"02_FG_{secrets.token_hex(8)}.png"
    video_gfx_name = f"video-gfx-{secrets.token_hex(8)}.mp4"
    html_assembly_name = f"gfx_html_{datetime.now().strftime('%Y%m%d_%H-%M-%S_%f')}"

    match order.request_type:
        case OrderRequestType.VIDEO_AUTO:
            order.background_name = background_name
            order.foreground_name = foreground_name
            order.video_gfx_name = video_gfx_name
            order.html_assembly_name = html_assembly_name

        case OrderRequestType.VIDEO_FILES:
            order.video_gfx_name = video_gfx_name
            order.html_assembly_name = html_assembly_name
            if order.background_screenshot:
                order.background_name = background_name

        case OrderRequestType.ONLY_SCREENSHOTS:
            order.background_name = background_name
            order.foreground_name = foreground_name

        case _:
            return
