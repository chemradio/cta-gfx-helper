import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver(driver_url: str) -> webdriver.Remote:
    chrome_options = Options()

    # chrome_options.add_argument("--allow-file-access-from-files")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.headless = True
    # chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("-–disable-gpu")

    vertical_resolution = int(os.environ.get("VERTICAL_RESOLUTION", 1080))
    horizontal_resolution = vertical_resolution / 9 * 16
    device_emulation = {
        "deviceMetrics": {
            "width": horizontal_resolution,
            "height": vertical_resolution,
            "pixelRatio": 1,
        },
    }
    chrome_options.add_experimental_option("mobileEmulation", device_emulation)
    driver = webdriver.Remote(driver_url, options=chrome_options)
    return driver
