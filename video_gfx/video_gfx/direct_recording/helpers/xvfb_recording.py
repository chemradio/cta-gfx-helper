import subprocess
import time
from pathlib import Path

import config

VIDEO_SIZE = f"1920x1080"
DISPLAY_CONTAINER_NAME = "selenium_webhost"
DISPLAY_NUM = 99
FRAME_RATE = 50
CODEC = "libx264"
PRESET = "ultrafast"


def record_selenium_xvfb(
    output_path: Path | str,
    record_duration_seconds: int | float = 20,
    audio_path: Path | str | None = None,
):
    # Define the ffmpeg command as a list of strings
    ffmpeg_command_pre_audio = [
        "ffmpeg",
        "-y",
        "-f",
        "x11grab",
        "-draw_mouse",
        "0",
        "-video_size",
        VIDEO_SIZE,
        "-r",
        str(FRAME_RATE),
        "-i",
        "video-gfx-selenium:99.0+nomouse",
    ]

    ffmpeg_audio = (
        [
            "-i",
            str(audio_path),
            # "-itsoffset",
            # str(config.AUDIO_OFFSET),
            # "-map",
            # "0:v",
            # "-map",
            # "1:a",
        ]
        if audio_path
        else []
    )

    ffmpeg_post_audio = [
        # "-vf",
        # "tinterlace=interleave_top,fieldorder=tff,scale=out_color_matrix=bt709:out_range=limited",
        # "scale=out_color_matrix=bt709:out_range=limited",
        "-codec:v",
        CODEC,
        "-preset",
        PRESET,
        "-tune",
        "zerolatency",
        "-pix_fmt",
        "yuv420p",
        "-color_range",
        "1",
        # "-video_bitrate",
        # str(config.VIDEO_BITRATE_BPS),
        # "-audio_bitrate",
        # str(config.AUDIO_BITRATE_BPS),
        "-crf",
        "13",
        # "-movflags",
        # "+write_colr",
        # "-bsf:v",
        # "h264_metadata=video_full_range_flag=0",
        # "-qp",
        # "0",
        str(output_path),
    ]

    ffmpeg_command = [*ffmpeg_command_pre_audio, *ffmpeg_audio, *ffmpeg_post_audio]

    # Start the ffmpeg process
    ffmpeg_process = subprocess.Popen(
        ffmpeg_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    try:
        # Wait for a certain amount of time (e.g., 10 seconds)
        time.sleep(record_duration_seconds)

        # Send the 'q' keystroke to quit ffmpeg
        ffmpeg_process.stdin.write("q")
        ffmpeg_process.stdin.flush()

        # Wait for the process to finish
        ffmpeg_process.wait()

    except KeyboardInterrupt:
        # Handle Ctrl+C if the user wants to manually terminate the script
        print("User interrupted. Terminating ffmpeg process...")
        ffmpeg_process.send_signal(subprocess.signal.SIGINT)

    finally:
        # Close the stdin, stdout, and stderr streams
        ffmpeg_process.stdin.close()
        ffmpeg_process.stdout.close()
        ffmpeg_process.stderr.close()

    # Check if the process has terminated and get the return code
    return_code = ffmpeg_process.returncode

    if return_code == 0:
        print("ffmpeg process completed successfully.", flush=True)
    else:
        print(f"ffmpeg process terminated with an error (Exit code {return_code}).")
