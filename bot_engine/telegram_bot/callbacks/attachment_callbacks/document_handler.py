import secrets
from pprint import pprint

from pydub import AudioSegment
from telegram import Message

import config
from telegram_bot.callbacks.attachment_callbacks.attachment_exceptions import (
    WrongImageFormat,
)
from telegram_bot.callbacks.attachment_callbacks.utils.image_converter import (
    convert_image_file,
)
from telegram_bot.callbacks.attachment_callbacks.utils.pdf_converter import (
    convert_pdf_to_image,
)


async def document_handler(message: Message) -> str:
    save_file_name = f"user_{secrets.token_hex(8)}"

    # add extension for pdf
    if message.document.mime_type == "application/pdf":
        save_file_name = f"{save_file_name}.pdf"
        save_file_path = config.USER_FILES_FOLDER / save_file_name

        file = await message.document.get_file()
        await file.download_to_drive(
            custom_path=save_file_path,
            read_timeout=config.FILE_DOWNLOAD_TIMEOUT,
            write_timeout=config.FILE_DOWNLOAD_TIMEOUT,
            connect_timeout=config.FILE_DOWNLOAD_TIMEOUT,
            pool_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        )

        # convert the file
        await convert_pdf_to_image(save_file_path)
        return save_file_name

    # refuse all other formats except images
    if "image" not in message.document.mime_type:
        raise WrongImageFormat(message.document.mime_type)

    # get the file
    file = await message.document.get_file()
    await file.download_to_drive(
        custom_path=save_file_path,
        read_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        write_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        connect_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        pool_timeout=config.FILE_DOWNLOAD_TIMEOUT,
    )

    # convert the file
    file_extension = await convert_image_file(save_file_path)

    return f"{save_file_name}.{file_extension}"
