import pydantic
from enum import Enum
from dataclasses import field
from shared.orders.order_base import OrderBase
from shared.utils.generate_filename import generate_filename, FilenameType


class VideoGfxTemplate(str, Enum):
    RFE = "RFE"
    CT = "CT"
    CT_AUTO = "CT_AUTO"


class VideoGfxOrderIn(pydantic.BaseModel):
    quote_text: str | None = None
    quote_author: str | None = None
    bg_filename: str | None = None
    fg_filename: str | None = None
    audio_filename: str | None = None
    template: VideoGfxTemplate = VideoGfxTemplate.CT_AUTO
    secret_key: str | None = None


class VideoGfxOrder(OrderBase):
    quote_text: str | None = None
    quote_author: str | None = None
    bg_filename: str | None = None
    fg_filename: str | None = None
    audio_filename: str | None = None
    template: VideoGfxTemplate = VideoGfxTemplate.CT_AUTO

    # output
    videogfx_filename: str = field(
        default_factory=lambda: generate_filename(FilenameType.VIDEOGFX)
    )

    def to_dict(self):
        return {
            "quote_enabled": self.quote_enabled,
            "quote_text": self.quote_text,
            "quote_author": self.quote_author,
            "bg_filename": self.bg_filename,
            "fg_filename": self.fg_filename,
            "audio_filename": self.audio_filename,
            "template": self.template,
            "videogfx_filename": self.videogfx_filename,
        }.update(super().to_dict())
