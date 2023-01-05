from enum import Enum


class BGAnimation(Enum):
    BG_ONLY = "bgOnly"
    BG_SCROLL = "bgScroll"
    BG_ZOOM = "bgZoom"


class FGAnimation(Enum):
    FACEBOOK = "facebook"
    ZOOM = "photo"
    DOCUMENT = "document"
    NONE = "none"


class AnimationParameters:
    def __init__(
        self,
        bg_animation: BGAnimation = BGAnimation.BG_SCROLL,
        bg_path: str = str(),
        single_layer: bool = True,
        fg_animation: FGAnimation = FGAnimation.FACEBOOK,
        fg_path: str = str(),
        round_corners: bool = False,
        quote_enabled: bool = False,
        quote_text: str = str(),
        quote_author_enabled: str = str(),
        quote_author: str = str(),
        audio_enabled: bool = False,
        audio_path: str = str(),
        animation_duration: float = 30.0,
    ) -> None:
        self.bg_animation = bg_animation.value
        self.bg_path = bg_path
        self.single_layer = single_layer
        self.fg_animation = fg_animation.value
        self.fg_path = fg_path
        self.round_corners = round_corners
        self.quote_text = quote_text
        self.quote_enabled = quote_enabled if self.quote_text else False
        self.quote_author = quote_author
        self.quote_author_enabled = quote_author_enabled if self.quote_author else False
        self.audio_path = audio_path
        self.audio_enabled = audio_enabled if self.audio_path else False
        self.animation_duration = animation_duration

    def calc_duration(self):
        pass

    def to_object(self) -> str:
        output = {
            "singleLayer": self.single_layer,
            "backgroundClass": self.bg_animation,
            "backgroundPath": self.bg_path,
            "foregroundClass": self.fg_animation,
            "foregroundPath": self.fg_path,
            "roundCorners": self.round_corners,
            "quoteEnabled": self.quote_enabled,
            "quoteTextText": self.quote_text,
            "quoteAuthorText": self.quote_author,
            "audioEnabled": self.audio_enabled,
            "audioPath": self.audio_path,
            "animationDuration": self.animation_duration,
        }

        return output
