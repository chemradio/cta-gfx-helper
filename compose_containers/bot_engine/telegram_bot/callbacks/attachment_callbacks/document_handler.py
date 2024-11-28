from telegram import File, Message

from telegram_bot.callbacks.attachment_callbacks.attachment_exceptions import (
    WrongImageFormat,
)


async def document_handler(message: Message) -> File:
    # add extension for pdf
    if message.document.mime_type == "application/pdf":
        return await message.document.get_file(), message.document.mime_type

    # refuse all other formats except images
    if "image" not in message.document.mime_type:
        raise WrongImageFormat(message.document.mime_type)

    # get the file
    return await message.document.get_file(), message.document.mime_type
