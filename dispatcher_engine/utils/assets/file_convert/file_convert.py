from io import BytesIO

from fastapi import UploadFile

from utils.assets.file_convert.workers.audio_to_wav import convert_audio_to_wav
from utils.assets.file_convert.workers.pdf_to_png import convert_pdf_to_png
from utils.assets.file_convert.workers.word_to_png import convert_word_to_png


class UnconvertableFile(Exception):
    def __init__(self, filename):
        self.filename = filename
        super().__init__()

    def __str__(self):
        return f"Unable to convert file: {self.filename}"


async def convert_unsupported_file(upload_file: UploadFile) -> BytesIO:
    try:
        file_mime = upload_file.content_type
        if "audio" in file_mime:
            return await convert_audio_to_wav(upload_file)

        elif file_mime == "application/pdf":
            print("pdf detected")
            return await convert_pdf_to_png(upload_file)

        elif file_mime == "application/msword":
            raise UnconvertableFile(upload_file.filename)
            return await convert_word_to_png(upload_file)

    except Exception as e:
        raise UnconvertableFile(upload_file.filename)
        raise UnconvertableFile(upload_file.filename)
