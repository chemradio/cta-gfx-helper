import secrets
import uuid

from fastapi import UploadFile

from utils.assets.file_convert.workers.audio_to_wav import convert_audio_to_wav
from utils.assets.file_convert.workers.pdf_to_png import convert_pdf_to_png
from utils.assets.file_convert.workers.word_to_png import convert_word_to_png


def generate_random_filename(prefix: str = "user", extension: str = str()):
    random_name = str(uuid.uuid4())
    filename = f"{prefix}_{random_name}.{extension}"
    return filename


class UnconvertableFile(Exception):
    def __init__(self, filename):
        self.filename = filename
        super().__init__()

    def __str__(self):
        return f"Unable to convert file: {self.filename}"


async def convert_unsupported_file(upload_file: UploadFile) -> tuple[str, bytes]:
    try:
        file_mime = upload_file.content_type
        if "audio" in file_mime:
            file_bytes = convert_audio_to_wav(upload_file)
            extension = "wav"

        elif file_mime == "application/pdf":
            file_bytes = convert_pdf_to_png(upload_file)
            extension = "png"

        elif file_mime == "application/msword":
            raise UnconvertableFile(upload_file.filename)
            file_bytes = convert_word_to_png(upload_file)
            extension = "png"

    except:
        raise UnconvertableFile(upload_file.filename)

    filename = generate_random_filename(extension=extension)
    return filename, file_bytes
