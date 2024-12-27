from dataclasses import dataclass
from io import BytesIO


@dataclass
class VideoGFXResults:
    video: BytesIO | None = None
    success: bool = False
    error_message: str | None = None
