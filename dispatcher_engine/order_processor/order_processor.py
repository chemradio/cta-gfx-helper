from .container_processors import process_screenshots, process_videogfx
from .telegram_send.telegram_send import send_file_telegram


def process_order(order: dict): ...
