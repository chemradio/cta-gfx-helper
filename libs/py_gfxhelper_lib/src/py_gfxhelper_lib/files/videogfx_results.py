from dataclasses import dataclass
from io import BytesIO


@dataclass
class VideoGFXResults:
    video: BytesIO
    success: bool = False
    error_message: str | None = None
