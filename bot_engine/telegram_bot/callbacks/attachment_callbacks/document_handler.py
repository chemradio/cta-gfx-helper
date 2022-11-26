from pprint import pprint
import config
from pydub import AudioSegment
from telegram import Message
from telegram_bot.callbacks.attachment_callbacks.attachment_exceptions import (
    WrongImageFormat,
)
from telegram_bot.callbacks.attachment_callbacks.utils.image_converter import (
    convert_image_file,
)
from telegram_bot.callbacks.attachment_callbacks.utils.pdf_converter import (
    convert_pdf_to_image,
)


async def document_handler(message: Message, save_file_name: str) -> str:
    # add extension for pdf
    if message.document.mime_type == "application/pdf":
        save_file_name = f"{save_file_name}.pdf"
        file = await message.document.get_file()
        await file.download(
            custom_path=save_file_name,
            read_timeout=config.FILE_DOWNLOAD_TIMEOUT,
            write_timeout=config.FILE_DOWNLOAD_TIMEOUT,
            connect_timeout=config.FILE_DOWNLOAD_TIMEOUT,
            pool_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        )

        # convert the file
        await convert_pdf_to_image(save_file_name)
        return save_file_name

    # refuse all other formats except images
    if "image" not in message.document.mime_type:
        raise WrongImageFormat(message.document.mime_type)

    # get the file
    file = await message.document.get_file()
    await file.download(
        custom_path=save_file_name,
        read_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        write_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        connect_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        pool_timeout=config.FILE_DOWNLOAD_TIMEOUT,
    )

    # convert the file
    save_file_name = await convert_image_file(save_file_name)
    return save_file_name
