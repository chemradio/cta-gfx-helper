import ffmpeg
import interlinks



PATH_PNG = '/Users/tim/Desktop/ffmpeg_test/input/png_sequence'
PATH_MP4 = '/Users/tim/Desktop/ffmpeg_test/input/ae-stitch.mp4'

OUTPUT_PATH_STITCH = '/Users/tim/Desktop/ffmpeg_test/output/ff-stitch.mp4'

output_params = {
    "video_bitrate": interlinks.VIDEO_BITRATE_BPS,
    "audio_bitrate": interlinks.AUDIO_BITRATE_BPS,
    "crf": 15,
    "vcodec": 'libx264',
    "pix_fmt": 'yuv420p',
    "movflags": '+write_colr',
    "vf":"scale=out_color_matrix=bt709:out_range=limited",

    # "vf":"scale=out_color_matrix=bt2020:out_range=limited",

    # "sws_flags": "spline+accurate_rnd+full_chroma_int",
    # "vf": "colormatrix=bt2020:bt709",
    # "color_range": 1,
    # "colorspace": 5,
    # "color_primaries": 1,
    # "color_trc": 192,
    # "bsf:v": "h264_metadata=video_full_range_flag=0",
}

def stitch_images():
    video_input = ffmpeg.input(f'{PATH_PNG}/*.png', pattern_type='glob',
                                framerate=25,
                                # pix_fmt='rgba',
                                )
    output = ffmpeg.output(video_input, OUTPUT_PATH_STITCH,
                            **output_params)
    output.run()
    

def reexport_video():
    ...

if __name__ == '__main__':
    import os
    os.remove(OUTPUT_PATH_STITCH)

    stitch_images()
    ...