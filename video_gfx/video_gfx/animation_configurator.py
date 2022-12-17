from video_gfx.animation_class_enums import (
    BGAnimation,
    FGAnimation,
    AnimationParameters,
)
from pydub import AudioSegment
from video_gfx.helpers.utils import get_image_orientation
import config
from video_gfx.helpers.enums import ImageOrientation


def create_animation_parameters(order):
    bg_path = order.get("bg_path", "")
    fg_path = order.get("fg_path", "")
    audio_enabled = order.get("audio_enabled", False)

    audio_path: str = order.get("audio_path", "")
    quote_enabled = order.get("quote_enabled", False)

    animation_duration = 30

    if audio_path:
        audio_file = AudioSegment.from_file(audio_path, audio_path[-3:])
        audio_duration = audio_file.duration_seconds
        animation_duration = float(config.AUDIO_OFFSET) + float(audio_duration)

    quote_text = order.get("quote_text", "")
    quote_author_enabled = order.get("quote_author_enabled", False)
    quote_author = order.get("quote_author_text", "")
    round_corners = order.get("round_corners_enabled", True)
    single_layer = not order.get("is_two_layer", False)

    request_type = order.get("request_type")

    # manual mode
    if request_type == "video_files":
        bg_ani_temp = order.get("bg_animation", "")
        fg_ani_temp = order.get("fg_animation", "")

        # configure manual bg animation
        if not bg_ani_temp or (bg_ani_temp == "scroll"):
            bg_animation = BGAnimation.BG_SCROLL
        else:
            bg_animation = BGAnimation.BG_ZOOM

        # configure manual fg animation
        if not fg_ani_temp:
            fg_animation = FGAnimation.ZOOM
        elif fg_ani_temp == "facebook":
            fg_animation = FGAnimation.FACEBOOK
        elif fg_ani_temp == "document":
            fg_animation = FGAnimation.DOCUMENT
        elif fg_ani_temp in ("twitter", "instagram", "telegram", "photo"):
            fg_animation = FGAnimation.ZOOM
        else:
            fg_animation = FGAnimation.NONE

    # auto mode
    elif request_type == "video_auto":
        link_type = order.get("link_type")
        fg_temp_path = order.get("fg_path")

        if (link_type == "scroll") or (not fg_temp_path):
            bg_animation = BGAnimation.BG_ONLY
            single_layer = True
            fg_animation = FGAnimation.NONE

        else:
            bg_animation == BGAnimation.BG_SCROLL

            fg_orientation = get_image_orientation(fg_temp_path)
            if fg_orientation == ImageOrientation.HORIZONTAL:
                fg_animation == FGAnimation.ZOOM
            else:
                fg_animation == FGAnimation.FACEBOOK

    animation_parameters = AnimationParameters(
        bg_animation=bg_animation,
        bg_path=bg_path,
        single_layer=single_layer,
        fg_animation=fg_animation,
        fg_path=fg_path,
        round_corners=round_corners,
        quote_enabled=quote_enabled,
        quote_text=quote_text,
        quote_author_enabled=quote_author_enabled,
        quote_author=quote_author,
        audio_enabled=audio_enabled,
        audio_path=audio_path,
        animation_duration=animation_duration,
    )
    return animation_parameters