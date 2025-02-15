import time
from time import perf_counter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
    driver.get(target_url)
    time.sleep(2)
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    for frame in range(start_frame, end_frame + 1):
        progress_frame = linear_interpolation(interpolation_data, frame)
        driver.execute_script(f"timeline.progress({progress_frame})")
        driver.save_screenshot(f"{png_path}/{frame:04}.png")
    driver.quit()
