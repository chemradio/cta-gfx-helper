import ffmpeg

encode_settings = {
    "s": "1920x1080",
    "crf": 13,
    "vcodec": "libx264",
    "pix_fmt": "yuv420p",
    "color_range": 1,
    "movflags": "+write_colr",
    "vf": "scale=out_color_matrix=bt709:out_range=limited",
    "bsf:v": "h264_metadata=video_full_range_flag=0",
}


def stitch_images(
    image_folder_path: str,
    output_path: str = "",
    audio_path: str = "",
    video_bitrate: int = 10_000_000,
    audio_bitrate: int = 256_000,
    audio_delay: float = 0.3,
) -> None:
    video_input = ffmpeg.input(
        f"{image_folder_path}/*.png",
        pattern_type="glob",
        framerate=25,
        pix_fmt="rgba",
    )
    output = ffmpeg.output(video_input, output_path, **encode_settings)

    if audio_path:
        audio_input = ffmpeg.input(audio_path, itsoffset=audio_delay)
        output = ffmpeg.output(
            video_input,
            audio_input,
            output_path,
            **encode_settings.update(
                {
                    "video_bitrate": video_bitrate,
                    "audio_bitrate": audio_bitrate,
                }
            ),
        )

    output.run()
