from io import BytesIO
from .helper_types import (
    ConvertedFile,
    FileExtension,
    FileMimeType,
    AUDIO_EXTENSIONS,
    WORD_EXTENSIONS,
    IMAGE_EXTENSIONS,
)
from .workers import (
    convert_audio_to_wav,
    convert_pdf_to_png,
    convert_word_to_png,
    convert_image_to_png,
)


async def convert_unsupported_file(
    file_bytesio: BytesIO, original_extension: FileExtension
) -> ConvertedFile:
    if original_extension in AUDIO_EXTENSIONS:
        converted_bytesio = await convert_audio_to_wav(file_bytesio)
        converted_mime_type = FileMimeType.WAV

    if original_extension in IMAGE_EXTENSIONS:
        converted_bytesio = await convert_image_to_png(file_bytesio)
        converted_mime_type = FileMimeType.PNG

    if original_extension in WORD_EXTENSIONS:
        converted_bytesio = await convert_word_to_png(file_bytesio)
        converted_mime_type = FileMimeType.PNG

    if original_extension == FileExtension.PDF:
        converted_bytesio = await convert_pdf_to_png(file_bytesio)
        converted_mime_type = FileMimeType.PNG

    return ConvertedFile(bytesio=converted_bytesio, mime_type=converted_mime_type)
