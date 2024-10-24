from db_mongo.models.orders import Order

from ..container_processors import process_screenshots
from ..telegram_send.telegram_send import send_file_telegram


async def process_only_screenshots(order: Order):
    screenshots = await process_screenshots(screenshot_url=order.link)
    await send_file_telegram(order.telegram_id, screenshots.background, "1_background")
    if screenshots.foreground:
        await send_file_telegram(
            order.telegram_id, screenshots.foreground, "2_foreground"
        )
