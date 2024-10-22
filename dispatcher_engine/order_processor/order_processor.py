from types.orders import OrderRequestType, OrderSource, OrderStatus

from db_mongo.models.orders import Order

from .container_processors import process_screenshots, process_videogfx
from .telegram_send.telegram_send import send_file_telegram


async def process_order(order: Order):
    # fix quote and audio fields
    order.quote_enabled = True if order.quote_text else False
    order.audio_enabled = True if order.audio_file else False

    # process lightweight order types
    if order.request_type in [
        OrderRequestType.READTIME,
    ]:
        ...
        return

    # process screenshots
    if order.request_type in [
        OrderRequestType.ONLY_SCREENSHOTS,
        OrderRequestType.VIDEO_AUTO,
        OrderRequestType.VIDEO_MIXED,
    ]:
        screenshots = await process_screenshots(order)

        # exit if only screenshots requested
        if order.request_type == OrderRequestType.ONLY_SCREENSHOTS:
            await send_file_telegram(order, screenshots.background, "1_background")
            await send_file_telegram(order, screenshots.foreground, "2_foreground")
            return

        order.background_file = screenshots.background
        if order.request_type == OrderRequestType.VIDEO_AUTO:
            order.foreground_file = (
                screenshots.foreground if screenshots.foreground else None
            )

    # process video
    videogfx = await process_videogfx(order.__dict__())
    await send_file_telegram(order, videogfx.video_file, "3_video")
