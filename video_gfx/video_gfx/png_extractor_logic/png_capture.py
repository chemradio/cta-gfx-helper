import base64
import json
import time
from io import BytesIO
from pathlib import Path
from time import perf_counter

from selenium import webdriver

from video_gfx.png_extractor_logic.create_driver import create_driver
from video_gfx.png_extractor_logic.helpers.linear_interpolator import (
    linear_interpolation,
)


def png_capture(
    total_frames: int,
    range_tuple: tuple,
    png_path: str,
    target_url: str,
    driver_url: str,
) -> None:
    driver = create_driver(driver_url)
    interpolation_data = [[0, 0], [total_frames, 1]]
    start_frame, end_frame = range_tuple
    print("getting target url", flush=True)
    driver.get(target_url)
    time.sleep(2)
    print("starting extraction", flush=True)
    for frame in range(start_frame, end_frame + 1):
        progress_frame = linear_interpolation(interpolation_data, frame)
        driver.execute_script(f"timeline.progress({progress_frame})")

        t1 = perf_counter()
        driver.save_screenshot(f"{png_path}/{frame:04}.png")
        t2 = perf_counter()
        print(f"Selenium capture and save screenshot took: {t2-t1}", flush=True)

        print(f"Extracting png sequence: {progress_frame*100:.2f}% done", flush=True)
    driver.quit()
