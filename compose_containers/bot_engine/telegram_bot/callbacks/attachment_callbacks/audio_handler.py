import secrets

from pydub import AudioSegment
from telegram import File, Message

import config
from telegram_bot.callbacks.attachment_callbacks.attachment_exceptions import (
    AudioDurationExceeded,
    WrongAudioFormat,
)


async def audio_handler(message: Message) -> File:
    return await message.audio.get_file(), message.audio.mime_type
