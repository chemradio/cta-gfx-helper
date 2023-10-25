import multiprocessing
import os
import threading
import time

import config

from video_gfx.helpers.timeline_splitter import split_timeline_segments
from video_gfx.png_extractor_logic.create_driver import create_driver
from video_gfx.png_extractor_logic.png_capture import png_capture

FPS = 25
USE_REMOTE_SELENIUM = True


def extract_png_sequence(html_assembly_name: str) -> str:
    """Extracts PNG-sequence from html gsap animation.
    Returns path to a folder containing the sequence"""
    print("creating driver", flush=True)
    driver = create_driver(config.SELENIUM_CONTAINERS[0])
    driver.implicitly_wait(5)

    print("getting server url", flush=True)

    if USE_REMOTE_SELENIUM:
        html_assembly_server_url = f"{config.ASSET_SERVER_ACCESS_URL_FOR_REMOTES}/html_assemblies/{html_assembly_name}"
        SELENIUM_CONTAINERS = config.SELENIUM_CONTAINERS_REMOTE
    else:
        html_assembly_server_url = (
            f"{config.ASSET_SERVER_ACCESS_URL}/html_assemblies/{html_assembly_name}"
        )
        SELENIUM_CONTAINERS = config.SELENIUM_CONTAINERS_LOCAL

    print(f"{html_assembly_server_url=}", flush=True)

    target_url = f"{html_assembly_server_url}/main.html"
    print(f"{target_url=}", flush=True)
    driver.get(target_url)
    time.sleep(2)
    print(f"getting timeline duration", flush=True)

    timeline_duration = driver.execute_script("return timeline.duration()")
    driver.quit()

    print(f"splitting work", flush=True)
    total_frames = timeline_duration * FPS
    ranges = split_timeline_segments(
        int(total_frames), pieces=len(config.SELENIUM_CONTAINERS)
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
    for index, driver_url in enumerate(SELENIUM_CONTAINERS):
        if config.USE_THREADS:
            driver_thread_process = threading.Thread(
                target=png_capture,
                args=(
                    total_frames,
                    ranges[index],
                    png_path,
                    target_url,
                    driver_url,
                ),
                name="main_driver_thread",
            )
        else:
            driver_thread_process = multiprocessing.Process(
                target=png_capture,
                args=(
                    total_frames,
                    ranges[index],
                    png_path,
                    target_url,
                    driver_url,
                ),
                name="main_driver_thread",
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
