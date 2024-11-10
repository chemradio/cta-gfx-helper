from dataclasses import dataclass
from enum import Enum
from io import BytesIO


class FileType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"


@dataclass
class ContainerOutputFile:
    file_type: FileType
    bytes_io: BytesIO | None
    filename: str | None = None
    text: str | None = None
