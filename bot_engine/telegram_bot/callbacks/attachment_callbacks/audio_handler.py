import secrets

from pydub import AudioSegment
from telegram import Message

import config
from telegram_bot.callbacks.attachment_callbacks.attachment_exceptions import (
    AudioDurationExceeded,
    WrongAudioFormat,
)


async def audio_handler(message: Message) -> str:

    try:
        if message.audio.mime_type in ["audio/mpeg3", "audio/mpeg"]:
            extension = "mp3"
        elif message.audio.mime_type == "audio/x-wav":
            extension = "wav"
    except:
        raise WrongAudioFormat(format=message.audio.mime_type)

    save_file_name = f"user_{secrets.token_hex(8)}.{extension}"
    save_file_path = config.USER_FILES_FOLDER / save_file_name

    file = await message.audio.get_file()
    await file.download_to_drive(
        custom_path=save_file_path,
        read_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        write_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        connect_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        pool_timeout=config.FILE_DOWNLOAD_TIMEOUT,
    )

    #  check duration
    audio_file = AudioSegment.from_file(save_file_path, extension)
    if audio_file.duration_seconds > config.MAX_AUDIO_LENGTH:
        raise AudioDurationExceeded

    # convert file
    await convert_audio_file(save_file_path)
    return save_file_name


async def convert_audio_file(file_path: str) -> bool:
    try:
        audio_file = AudioSegment.from_file(file_path)
        with open(file_path, "wb") as out_file:
            audio_file.export(
                out_file,
                format="mp3",
                bitrate="256k",
                # parameters=[
                #     "-ac",
                #     "2",
                # ],
            )
        return True
    except:
        print("failed to convert the file")
        return False
