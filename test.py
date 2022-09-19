import ffmpeg
import interlinks


PATH_PNG = '/Users/tim/Desktop/ffmpeg_test/input/png_sequence'
PATH_MP4 = '/Users/tim/Desktop/ffmpeg_test/input/ae-stitch.mp4'

OUTPUT_PATH_STITCH = '/Users/tim/Desktop/ffmpeg_test/output/ff-stitch.mp4'

def stitch_images():
    video_input = ffmpeg.input(f'{PATH_PNG}/*.png', pattern_type='glob',
                                framerate=25,
                                pix_fmt='rgba',
                                )
    output = ffmpeg.output(video_input, OUTPUT_PATH_STITCH,
                            video_bitrate=interlinks.VIDEO_BITRATE_KBPS,
                            audio_bitrate=interlinks.AUDIO_BITRATE_KBPS,
                            crf=15,

                            # vcodec='libx264rgb',
                            # pix_fmt='rgb24',

                            vcodec='libx264',
                            pix_fmt='yuv420p',

                            # color_range=2,
                            # movflags= '+write_colr',

                            # add 420

                            # **{"bsf:v": "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=8:matrix_coefficients=1"}
                            )
    print(output.get_args())
    output.run()
    

def reexport_video():
    ...

if __name__ == '__main__':
    stitch_images()
    ...