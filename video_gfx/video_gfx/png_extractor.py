import multiprocessing
import os
import threading
import time

import config

from video_gfx.helpers.timeline_splitter import split_timeline_segments
from video_gfx.png_extractor_logic.create_driver import create_driver
from video_gfx.png_extractor_logic.png_capture import png_capture, png_capture_buffered

FPS = 25
USE_LOCAL_SELENIUM = True
USE_REMOTE_SELENIUM = os.getenv("USE_REMOTE_SELENIUM", False)


def extract_png_sequence(html_assembly_name: str) -> str:
    """Extracts PNG-sequence from html gsap animation.
    Returns path to a folder containing the sequence"""
    html_assembly_server_url_remote = f"{config.ASSET_SERVER_ACCESS_URL_FOR_REMOTES}/html_assemblies/{html_assembly_name}"
    html_assembly_server_url_local = (
        f"{config.ASSET_SERVER_ACCESS_URL}/html_assemblies/{html_assembly_name}"
    )
    SELENIUM_CONTAINERS_LOCAL = (
        config.SELENIUM_CONTAINERS_LOCAL if USE_LOCAL_SELENIUM else []
    )
    SELENIUM_CONTAINERS_REMOTE = (
        config.SELENIUM_CONTAINERS_REMOTE if USE_REMOTE_SELENIUM else []
    )

    ALL_SELENIUM_CONTAINERS = [*SELENIUM_CONTAINERS_LOCAL, *SELENIUM_CONTAINERS_REMOTE]

    driver = create_driver(ALL_SELENIUM_CONTAINERS[0])
    driver.implicitly_wait(5)
    target_url_local = f"{html_assembly_server_url_local}/main.html"
    target_url_remote = f"{html_assembly_server_url_remote}/main.html"

    driver.get(target_url_remote if USE_REMOTE_SELENIUM else target_url_local)
    time.sleep(2)
    print(f"getting timeline duration", flush=True)
    timeline_duration = driver.execute_script("return timeline.duration()")
    driver.quit()

    print(f"splitting work", flush=True)
    total_frames = timeline_duration * FPS
    ranges = split_timeline_segments(
        int(total_frames), pieces=len(ALL_SELENIUM_CONTAINERS)
    )

    print(f"generating png path", flush=True)
    # create a folder for png-sequence
    png_path = os.path.join(
        f"{config.HTML_ASSEMBLIES_FOLDER}/{html_assembly_name}", "png_sequence"
    )
    print(f"{png_path=}", flush=True)

    os.mkdir(png_path)

    # create webdriver threads / processes
    driver_threads_processes = list()
    for driver_url in SELENIUM_CONTAINERS_LOCAL:
        driver_thread_process = multiprocessing.Process(
            target=png_capture,
            args=(
                total_frames,
                ranges.pop(0),
                png_path,
                target_url_local,
                driver_url,
            ),
        )
        driver_threads_processes.append(driver_thread_process)

    for driver_url in SELENIUM_CONTAINERS_REMOTE:
        driver_thread_process = multiprocessing.Process(
            target=png_capture,
            args=(
                total_frames,
                ranges.pop(0),
                png_path,
                target_url_remote,
                driver_url,
            ),
        )
        driver_threads_processes.append(driver_thread_process)

    print("starting threads/processes", flush=True)
    for thread_process in driver_threads_processes:
        thread_process.start()
    print("threads/processes started", flush=True)

    for thread_process in driver_threads_processes:
        thread_process.join()

    print("threads/processes finished", flush=True)

    return png_path
