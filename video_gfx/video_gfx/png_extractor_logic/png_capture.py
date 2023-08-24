import time

from selenium import webdriver

from video_gfx.png_extractor_logic.helpers.linear_interpolator import (
    linear_interpolation,
)


def png_capture(
    total_frames: int,
    range_tuple: tuple,
    png_path: str,
    target_url: str,
    driver: webdriver.Remote,
) -> None:
    interpolation_data = [[0, 0], [total_frames, 1]]
    start_frame, end_frame = range_tuple
    print("getting target url", flush=True)
    driver.get(target_url)
    time.sleep(2)
    for frame in range(start_frame, end_frame + 1):
        progress_frame = linear_interpolation(interpolation_data, frame)
        driver.execute_script(f"timeline.progress({progress_frame})")
        driver.save_screenshot(f"{png_path}/{frame:04}.png")
        print(f"Extracting png sequence: {progress_frame*100:.2f}% done", flush=True)
    driver.quit()
