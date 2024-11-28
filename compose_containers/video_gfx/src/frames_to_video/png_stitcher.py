from pathlib import Path

import ffmpeg
from PIL import Image

from shared.utils.asset_file import AssetFile


def stitch_images(
    image_folder_path: Path,
    framerate: int | float,
    audio_file: AssetFile | None,
    output_path: Path | None = None,
    # video_bitrate: int = 10_000_000,
    # audio_bitrate: int = 256_000,
    audio_delay: float = 0.3,
) -> Path:
    def get_frame_size(image_folder_path: Path) -> tuple[int, int]:
        image = Image.open(next(image_folder_path.glob("*.png")))
        return image.size

    frame_size = get_frame_size(image_folder_path)

    encode_settings = {
        "s": f"{frame_size[0]}x{frame_size[1]}",
        "crf": 13,
        "vcodec": "libx264",
        "pix_fmt": "yuv420p",
        "color_range": 1,
        "movflags": "+write_colr",
        "vf": "scale=out_color_matrix=bt709:out_range=limited",
        "bsf:v": "h264_metadata=video_full_range_flag=0",
    }

    video_input = ffmpeg.input(
        f"{str(image_folder_path)}/*.png",
        pattern_type="glob",
        framerate=framerate,
        pix_fmt="rgba",
    )

    if not output_path:
        output_path = image_folder_path / "output.mp4"

    # audio
    audio_input = None
    if audio_file:
        audio_extension = audio_file.filename.split(".")[-1]
        temp_audio_file_path = image_folder_path / f"audio_file.{audio_extension}"
        with open(temp_audio_file_path, "wb") as f:
            f.write(audio_file.file.read())

        audio_input = ffmpeg.input(
            str(temp_audio_file_path), f=audio_extension.lower(), itsoffset=audio_delay
        )

    if audio_input:
        output = ffmpeg.output(
            video_input, audio_input, str(output_path), **encode_settings
        )
    else:
        output = ffmpeg.output(video_input, str(output_path), **encode_settings)

    output.run()

    return output_path
