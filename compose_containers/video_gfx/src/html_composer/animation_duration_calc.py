import pydub

from shared.utils.asset_file import AssetFile


def calculate_animation_duration(order: dict) -> float:
    default_duration = order["animation_duration"]

    # get audio file duration
    audio_file: AssetFile | None = order.get("audio_file")
    if audio_file:
        audio_file.file.seek(0)
        audio_segment = pydub.AudioSegment.from_file(
            audio_file.file, format=audio_file.filename.split(".")[-1].upper()
        )
        audio_duration = len(audio_segment) / 1000.0
        audio_file.file.seek(0)

        animation_duration = (
            audio_duration + order["audio_offset"] + order["videogfx_tail"]
        )
    else:
        animation_duration = default_duration

    return animation_duration
