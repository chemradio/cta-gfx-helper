from pathlib import Path
from typing import Optional

from pydub import AudioSegment

import config
from video_gfx.animation_class_enums import (
    AnimationParameters,
    BGAnimation,
    FGAnimation,
)
from video_gfx.helpers.enums import ImageOrientation
from video_gfx.helpers.utils import get_image_orientation


def create_animation_parameters(order):
    bg_name = order.get("background_name", "")
    fg_name = order.get("foreground_name", "")
    audio_name: str = order.get("audio_name", "")

    bg_path, fg_path, audio_path = find_files(bg_name, fg_name, audio_name)

    audio_enabled = order.get("audio_enabled", False)

    quote_enabled = order.get("quote_enabled", False)

    animation_duration = config.DEFAULT_ANIMATION_DURATION

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
        single_layer = not bool(fg_path)

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

        if (link_type == "scroll") or (not fg_path):
            bg_animation = BGAnimation.BG_ONLY
            single_layer = True
            fg_animation = FGAnimation.NONE

        else:
            single_layer = False

            bg_animation = BGAnimation.BG_SCROLL

            fg_orientation = get_image_orientation(fg_path)
            if fg_orientation == ImageOrientation.HORIZONTAL:
                fg_animation = FGAnimation.ZOOM
            else:
                fg_animation = FGAnimation.FACEBOOK

    animation_parameters = AnimationParameters(
        bg_animation=bg_animation,
        bg_path=str(bg_path),
        single_layer=single_layer,
        fg_animation=fg_animation,
        fg_path=str(fg_path),
        round_corners=round_corners,
        quote_enabled=quote_enabled,
        quote_text=quote_text,
        quote_author_enabled=quote_author_enabled,
        quote_author=quote_author,
        audio_enabled=audio_enabled,
        audio_path=str(audio_path),
        animation_duration=animation_duration,
    )
    return animation_parameters


def find_files(
    bg_name: str = "", fg_name: str = "", audio_name: str = ""
) -> tuple[Optional[Path]]:
    bg_path, fg_path, audio_path = "", "", ""

    folders = (config.SCREENSHOTS_FOLDER, config.USER_FILES_FOLDER)

    def find_path(file_name, search_folders) -> Optional[Path]:
        for folder in search_folders:
            if (folder / file_name).exists():
                return folder / file_name

    if bg_name:
        bg_path = find_path(bg_name, folders)

    if fg_name:
        fg_path = find_path(fg_name, folders)

    if audio_name:
        audiog_path = find_path(audio_name, folders)

    return bg_path, fg_path, audio_path
