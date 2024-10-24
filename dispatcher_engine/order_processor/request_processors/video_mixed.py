from db_mongo.models.orders import Order

from ..container_processors import process_screenshots, process_videogfx
from ..telegram_send.telegram_send import send_file_telegram


async def process_video_mixed(order: Order):
    screenshots = await process_screenshots(screenshot_url=order.link)
    return await process_videogfx(
        quote_text=order.quote_text,
        quote_author=order.quote_author_text,
        background_file=screenshots.background,
        foreground_file=order.foreground_file,
        audio_file=order.audio_file,
    ).video
