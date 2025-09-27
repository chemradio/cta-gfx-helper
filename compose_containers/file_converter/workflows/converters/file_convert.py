from .workers import (
    convert_audio_to_wav,
    convert_pdf_to_png,
    convert_word_to_png,
    convert_image_to_png,
)
from py_gfxhelper_lib.files import AssetFile


import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def convert_unsupported_file(
    file: AssetFile,
) -> AssetFile:
    AUDIO_EXTENSIONS = ("wav", "mp3", "ogg")
    IMAGE_EXTENSIONS = ("png", "jpg", "jpeg")
    WORD_EXTENSIONS = ("doc", "docx")

    logger.info(f"Attempting conversion for file: {file.extension}")

    if file.extension in AUDIO_EXTENSIONS:
        logger.info("Detected audio file, converting to WAV format")
        converted_bytesio = await convert_audio_to_wav(file.bytesio)
        converted_mime_type = "audio/wav"

    if file.extension in IMAGE_EXTENSIONS:
        logger.info("Detected image file, converting to PNG format")
        converted_bytesio = await convert_image_to_png(file.bytesio)
        converted_mime_type = "image/png"

    if file.extension in WORD_EXTENSIONS:
        logger.info("Detected Word file, converting to PNG format")
        converted_bytesio = await convert_word_to_png(file.bytesio)
        converted_mime_type = "image/png"

    if file.extension == "pdf":
        logger.info("Detected PDF file, converting to PNG format")
        converted_bytesio = await convert_pdf_to_png(file.bytesio)
        converted_mime_type = "image/png"

    logger.info(
        f"File conversion successful: {file.extension} to {converted_mime_type}"
    )
    logger.info(
        f"Converted file size in MB is: {converted_bytesio.getbuffer().nbytes / (1024 * 1024)}"
    )
    converted_bytesio.seek(0)

    return AssetFile(bytes_or_bytesio=converted_bytesio, mime_type=converted_mime_type)
