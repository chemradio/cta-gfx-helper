from dataclasses import dataclass
from enum import Enum
from io import BytesIO

ext_map = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "wav": "audio/wav",
    "mp3": "audio/mpeg",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

mime_map = {
    "application/pdf": "pdf",
    "image/png": "png",
    "image/jpeg": "jpg",
    "audio/wav": "wav",
    "audio/mpeg": "mp3",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}


class FileMimeType(str, Enum):
    PDF = "application/pdf"
    PNG = "image/png"
    JPG = "image/jpeg"
    JPEG = "image/jpeg"
    WAV = "audio/wav"
    MP3 = "audio/mpeg"
    OGG = "audio/ogg"
    DOC = "application/msword"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class FileExtension(str, Enum):
    PDF = "pdf"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    WAV = "wav"
    MP3 = "mp3"
    OGG = "ogg"
    DOC = "doc"
    DOCX = "docx"


class FileType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    WORD = "word"
    PDF = "pdf"


AUDIO_EXTENSIONS = (FileExtension.WAV, FileExtension.MP3, FileExtension.OGG)
IMAGE_EXTENSIONS = (FileExtension.PNG, FileExtension.JPG, FileExtension.JPEG)
WORD_EXTENSIONS = (FileExtension.DOC, FileExtension.DOCX)


@dataclass
class ConvertedFile:
    bytesio: BytesIO
    mime_type: FileMimeType
