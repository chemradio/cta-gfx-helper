import time
from time import perf_counter

from src.helpers import linear_interpolation

from .custom_driver import create_driver


def png_capture(
    total_frames: int,
    range_tuple: tuple[int, int],
    png_path: str,
    target_url: str,
    driver_url: str,
    frame_width: int,
    frame_height: int,
) -> None:

    driver = create_driver(driver_url, frame_width, frame_height)
    interpolation_data = [[0, 0], [total_frames, 1]]
    start_frame, end_frame = range_tuple
    print("getting target url", flush=True)
    driver.get(target_url)
    time.sleep(2)
    print("starting extraction", flush=True)
    o1 = perf_counter()
    for frame in range(start_frame, end_frame + 1):
        progress_frame = linear_interpolation(interpolation_data, frame)
        driver.execute_script(f"timeline.progress({progress_frame})")

        t1 = perf_counter()
        driver.save_screenshot(f"{png_path}/{frame:04}.png")
        t2 = perf_counter()
        print(f"Selenium capture and save screenshot took: {t2-t1}", flush=True)

        print(f"Extracting png sequence: {progress_frame*100:.2f}% done", flush=True)
    o2 = perf_counter()
    print(f"Extraction in thread took: {o2-o1}", flush=True)
    driver.quit()
