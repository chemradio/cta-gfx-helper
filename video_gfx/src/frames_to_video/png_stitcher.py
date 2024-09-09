from pathlib import Path

import ffmpeg
from fastapi import UploadFile
from PIL import Image


def stitch_images(
    image_folder_path: Path,
    framerate: int | float,
    output_path: Path | None,
    audio_file: UploadFile | None,
    video_bitrate: int = 10_000_000,
    audio_bitrate: int = 256_000,
    audio_delay: float = 0.3,
) -> Path:

    # determine frame size
    image = Image.open(next(image_folder_path.glob("*.png")))
    frame_size = image.size

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

    # audio
    if audio_file:
        audio_extension = audio_file.filename.split(".")[-1]
        audio_input = ffmpeg.input(
            audio_file.file, f=audio_extension.lower(), itsoffset=audio_delay
        )
    else:
        audio_input = None

    if not output_path:
        output_path = image_folder_path / "output.mp4"

    output = ffmpeg.output(video_input, audio_input, str(output_path), encode_settings)
    output.run()
