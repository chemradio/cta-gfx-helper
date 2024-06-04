from dataclasses import dataclass

from .screenshot import Screenshot


@dataclass
class ScreenshotResults:
    success: bool = False
    background: Screenshot | None = None
    foreground: Screenshot | None = None
    two_layer: bool = False
    error_message: str | None = None

    def to_dict(self):
        return {
            "success": self.success,
            "background": "BytesIO object placeholder",
            "foreground": "BytesIO object placeholder",
            "two_layer": self.two_layer,
            "error_message": self.error_message,
        }
