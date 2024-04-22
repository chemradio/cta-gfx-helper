import config
import ffmpeg

encode_settings = {
    "pix_fmt": "yuv420p",
    "vf": "scale=in_color_matrix=bt709:out_color_matrix=bt709",
    "c:v": "libx264",
    "preset": "slower",
    "colorspace": "bt709",
    "color_primaries": "bt709",
    "color_trc": "iec61966-2-1",
    "c": "copy",
    "bsf": "h264_metadata=video_full_range_flag=0",
    "crf": 15,
}


def stitch_images(
    image_folder_path: str, output_path: str = "", audio_path: str = ""
) -> None:
    video_input = ffmpeg.input(
        f"{image_folder_path}/*.png",
        pattern_type="glob",
        framerate=25,
        pix_fmt="rgba",
    )
    output = ffmpeg.output(video_input, output_path, **encode_settings)

    if audio_path:
        audio_input = ffmpeg.input(audio_path, itsoffset=config.AUDIO_OFFSET)
        output = ffmpeg.output(video_input, audio_input, output_path, **encode_settings)

    output.run()
