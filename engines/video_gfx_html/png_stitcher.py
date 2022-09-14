from email.mime import audio
import ffmpeg
import interlinks

bitrate = {
    'video_bitrate': f"{interlinks.VIDEO_BITRATE_KBPS}k",
    'audio_bitrate': f"{interlinks.AUDIO_BITRATE_KBPS}k",
}

def stitch_images(image_folder_path: str, output_path: str = '', audio_path: str = '') -> None:
    video_input = ffmpeg.input(f'{image_folder_path}/*.png', pattern_type='glob', framerate=25)
    output = ffmpeg.output(video_input, output_path, **bitrate)

    if audio_path:
        audio_input = ffmpeg.input(audio_path, itsoffset=interlinks.AUDIO_OFFSET)
        output = ffmpeg.output(video_input, audio_input, output_path, **bitrate)
    
    output.run()
    




if __name__ == '__main__':
    proc = stitch_images(
        '/Users/tim/code/cta-gfx-telegram-bot/assets/html_assemblies/gfx_html_20220814_17-02-51_076061/png_sequence',
        '/Users/tim/code/cta-gfx-telegram-bot/assets/video_exports/Tim-gfx.mp4',
        '/Users/tim/Desktop/temp/test_speech.mp3'
    )
    print(proc)