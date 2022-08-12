import ffmpeg


def stitch_images(image_folder_path: str, output_path: str = '') -> None:
    """Returns a ready-video path."""
    (
        ffmpeg
        # .filter("tinterlace", "interleave_top")
        # .filter("fieldorder", "tff")
        .input(f'{image_folder_path}/*.png', pattern_type='glob', framerate=25)
        .output(f'{output_path}.mp4')
        .run()
    )




if __name__ == '__main__':
    stitch_images(
        '/Users/tim/code/ae-to-html/html/html_assemblies/gfx_html_20220811_02-21-37_365727/png_sequence',
        'testerMovie'
    )