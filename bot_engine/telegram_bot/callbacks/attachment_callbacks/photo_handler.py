import secrets

from telegram import File, Message

import config
from telegram_bot.callbacks.attachment_callbacks.utils.image_converter import (
    convert_image_file,
)


async def photo_handler(message: Message) -> File:
    # find the best quality photo
    photo_file_size = 0
    best_quality_photo_index = 0
    for index, photo in enumerate(message.photo):
        if photo["file_size"] > photo_file_size:
            photo_file_size = photo["file_size"]
            best_quality_photo_index = index

    return await message.photo[best_quality_photo_index].get_file(), "image/jpeg"
