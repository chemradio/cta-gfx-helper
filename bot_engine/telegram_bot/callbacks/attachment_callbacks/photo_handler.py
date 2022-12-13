from telegram import Message

import config
from telegram_bot.callbacks.attachment_callbacks.utils.image_converter import (
    convert_image_file,
)


async def photo_handler(message: Message, save_file_name: str) -> str:
    # find the best quality photo
    photo_file_size = 0
    best_quality_photo_index = 0
    for index, photo in enumerate(message.photo):
        if photo["file_size"] > photo_file_size:
            photo_file_size = photo["file_size"]
            best_quality_photo_index = index

    # save the photo
    save_file_name = f"{save_file_name}.png"
    photo = await message.photo[best_quality_photo_index].get_file()
    await photo.download_to_drive(
        custom_path=save_file_name,
        read_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        write_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        connect_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        pool_timeout=config.FILE_DOWNLOAD_TIMEOUT,
    )

    # convert photo
    save_file_name = await convert_image_file(save_file_name)
    return save_file_name
