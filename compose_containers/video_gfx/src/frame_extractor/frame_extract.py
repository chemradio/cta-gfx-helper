import json
import multiprocessing
import os
from pathlib import Path

from src.helpers import split_timeline_segments

from .png_capture import png_capture

FPS = 25


def extract_frame_images(
    html_assembly_path: Path,
    remote_driver_url_list: list[str],
    framerate: int | float,
    assembly_server_url: str,
) -> Path:
    """Extracts PNG-sequence from html gsap animation.
    Returns path to a folder containing the sequence"""

    target_url = f"{assembly_server_url}/storage/{html_assembly_path.name}/main.html"

    # get timeline duration and vertical resolution
    with open(html_assembly_path / "config.json", "rt") as json_config_file:
        animation_config = json.load(json_config_file)
        timeline_duration = animation_config["animationDuration"]
        vertical_resolution = animation_config["verticalResolution"]

    total_frames = timeline_duration * framerate
    ranges = split_timeline_segments(
        int(total_frames), pieces=len(remote_driver_url_list)
    )

    # create a folder for png-sequence
    png_path = html_assembly_path / "png_sequence"
    os.mkdir(png_path)

    # create webdriver threads / processes
    driver_processes = list()
    for driver_url in remote_driver_url_list:
        driver_thread_process = multiprocessing.Process(
            target=png_capture,
            args=(
                total_frames,
                ranges.pop(0),
                png_path,
                target_url,
                driver_url,
                int(vertical_resolution) / 9 * 16,
                int(vertical_resolution),
            ),
        )
        driver_processes.append(driver_thread_process)

    for thread_process in driver_processes:
        thread_process.start()

    for thread_process in driver_processes:
        thread_process.join()

    return png_path
