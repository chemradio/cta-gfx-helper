from telegram import File, Message


async def audio_handler(message: Message) -> tuple[File, str]:
    return await message.audio.get_file(), message.audio.mime_type
