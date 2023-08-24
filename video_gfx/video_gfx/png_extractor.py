import os
import threading
import time

import config
from video_gfx.helpers.timeline_splitter import split_timeline_segments
from video_gfx.png_extractor_logic.create_driver import create_driver
from video_gfx.png_extractor_logic.png_capture import png_capture

FPS = 25


def extract_png_sequence(html_assembly_name: str) -> str:
    """Extracts PNG-sequence from html gsap animation.
    Returns path to a folder containing the sequence"""
    driver = create_driver(config.SELENIUM_CONTAINERS[0])
    driver.implicitly_wait(5)

    html_assembly_server_url = (
        f"{config.ASSET_SERVER_ACCESS_URL}/html_assemblies/{html_assembly_name}"
    )

    target_url = f"{html_assembly_server_url}/main.html"
    driver.get(target_url)
    time.sleep(2)
    timeline_duration = driver.execute_script("return timeline.duration()")
    driver.quit()

    total_frames = timeline_duration * FPS
    ranges = split_timeline_segments(
        int(total_frames), pieces=len(config.SELENIUM_CONTAINERS)
    )

    # create a folder for png-sequence
    png_path = os.path.join(
        f"{config.HTML_ASSEMBLIES_FOLDER}/{html_assembly_name}", "png_sequence"
    )
    os.mkdir(png_path)

    # create webdriver threads
    driver_threads = list()
    for index, driver_url in enumerate(config.SELENIUM_CONTAINERS):
        driver = create_driver(driver_url)
        driver_thread = threading.Thread(
            target=png_capture,
            args=(
                total_frames,
                ranges[index],
                png_path,
                target_url,
                driver,
            ),
            name="main_driver_thread",
        )
        driver_threads.append(driver_thread)

    print("starting threads", flush=True)
    for thread in driver_threads:
        thread.start()
    print("threads started", flush=True)

    for thread in driver_threads:
        thread.join()
    # support_driver_thread.join()
    print("threads finished", flush=True)

    return png_path
