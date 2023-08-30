import ffmpeg

import config

encode_settings = {
    "video_bitrate": config.VIDEO_BITRATE_BPS,
    "audio_bitrate": config.AUDIO_BITRATE_BPS,
    "crf": 13,
    "vcodec": "libx264",
    "pix_fmt": "yuv420p",
    "color_range": 1,
    "movflags": "+write_colr",
    "vf": "scale=out_color_matrix=bt709:out_range=limited,tinterlace=interleave_top,fieldorder=tff",
    "bsf:v": "h264_metadata=video_full_range_flag=0",
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
