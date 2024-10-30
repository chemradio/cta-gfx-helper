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
    filename: str | None = None
    file_type: FileType
    bytes_io: BytesIO
