import subprocess
import time

VIDEO_SIZE = f"1920x1080"
FRAME_RATE = 50
CODEC = "libx264"
PRESET = "ultrafast"


def perform_recording():
    # Define the ffmpeg command as a list of strings
    ffmpeg_command = [
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
        "chromium:0",
        # "chromium:0.0+nomouse",
        "-codec:v",
        CODEC,
        # "-preset",
        # PRESET,
        # "-tune",
        # "zerolatency",
        # "-pix_fmt",
        # "yuv420p",
        # "-color_range",
        # "1",
        "-crf",
        "13",
        "recording.mp4",
    ]

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
        time.sleep(15)

        # Send the 'q' keystroke to quit ffmpeg
        ffmpeg_process.stdin.write("q")
        ffmpeg_process.stdin.flush()
        stdout, stderr = ffmpeg_process.communicate()
        
    finally:
        # Print the stderr output
        print("ffmpeg stderr output:")
        print(stderr)

    # Check if the process has terminated and get the return code
    return_code = ffmpeg_process.returncode

    if return_code == 0:
        print("ffmpeg process completed successfully.", flush=True)
    else:
        print(f"ffmpeg process terminated with an error (Exit code {return_code}).")
