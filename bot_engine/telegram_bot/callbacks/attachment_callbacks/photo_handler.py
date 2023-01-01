import secrets

from telegram import Message

import config
from telegram_bot.callbacks.attachment_callbacks.utils.image_converter import (
    convert_image_file,
)


async def photo_handler(message: Message) -> str:
    save_file_name = f"user_{secrets.token_hex(8)}"
    save_file_path = config.USER_FILES_FOLDER / save_file_name

    # find the best quality photo
    photo_file_size = 0
    best_quality_photo_index = 0
    for index, photo in enumerate(message.photo):
        if photo["file_size"] > photo_file_size:
            photo_file_size = photo["file_size"]
            best_quality_photo_index = index

    # save the photo
    photo = await message.photo[best_quality_photo_index].get_file()
    await photo.download_to_drive(
        custom_path=save_file_path,
        read_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        write_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        connect_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        pool_timeout=config.FILE_DOWNLOAD_TIMEOUT,
    )

    # convert photo
    extension = await convert_image_file(save_file_path)
    return f"{save_file_name}.{extension}"
