from io import BytesIO
from .workers import (
    convert_audio_to_wav,
    convert_pdf_to_png,
    convert_word_to_png,
    convert_image_to_png,
)
from py_gfxhelper_lib.files import AssetFile


async def convert_unsupported_file(
    file_bytesio: BytesIO, original_extension: str
) -> AssetFile:
    AUDIO_EXTENSIONS = ("wav", "mp3", "ogg")
    IMAGE_EXTENSIONS = ("png", "jpg", "jpeg")
    WORD_EXTENSIONS = ("doc", "docx")

    if original_extension in AUDIO_EXTENSIONS:
        converted_bytesio = await convert_audio_to_wav(file_bytesio)
        converted_mime_type = "audio/wav"

    if original_extension in IMAGE_EXTENSIONS:
        converted_bytesio = await convert_image_to_png(file_bytesio)
        converted_mime_type = "image/png"

    if original_extension in WORD_EXTENSIONS:
        converted_bytesio = await convert_word_to_png(file_bytesio)
        converted_mime_type = "image/png"

    if original_extension == "pdf":
        converted_bytesio = await convert_pdf_to_png(file_bytesio)
        converted_mime_type = "image/png"

    return AssetFile(bytes_or_bytesio=converted_bytesio, mime_type=converted_mime_type)
