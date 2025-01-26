from telegram import File, Message


async def document_handler(message: Message) -> tuple[File, str]:
    # add extension for pdf
    if message.document.mime_type == "application/pdf":
        return await message.document.get_file(), "application/pdf"

    if (
        message.document.mime_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        return (
            await message.document.get_file(),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    # refuse all other formats except images
    if "image" not in message.document.mime_type:
        raise Exception(f"Image format {message.document.mime_type} is not supported.")

    # get the file
    return await message.document.get_file(), message.document.mime_type
