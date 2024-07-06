import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver(
    remote_driver_url: str, frame_width: int, frame_height: int
) -> webdriver.Remote:
    chrome_options = Options()

    # chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.headless = True

    device_emulation = {
        "deviceMetrics": {
            "width": frame_width,
            "height": frame_height,
            "pixelRatio": 1,
        },
    }
    chrome_options.add_experimental_option("mobileEmulation", device_emulation)
    driver = webdriver.Remote(remote_driver_url, options=chrome_options)
    return driver
