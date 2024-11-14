from enum import Enum
from io import BytesIO

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse


class FileFormat(str, Enum):
    pdf = "pdf"
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
    wav = "wav"
    mp3 = "mp3"
    doc = "doc"
    docx = "docx"


mime_map = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "wav": "audio/wav",
    "mp3": "audio/mpeg",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


app = FastAPI()


@app.post("/")
def convert_file(
    file: UploadFile = File(...),
    target_format: FileFormat = Form(...),
    secret_key: str | None = Form(None),
) -> FileResponse:
    original_format = file.filename.split(".")[-1]
    file_bytesio = BytesIO(file.file.read())

    converted_file = convert_file(file_bytesio, original_format, target_format)
    return FileResponse(
        converted_file,
        media_type=mime_map[target_format],
        filename=file.filename,
    )


def convert_file(
    file_bytesio: BytesIO, original_format, target_format: str
) -> BytesIO: ...
