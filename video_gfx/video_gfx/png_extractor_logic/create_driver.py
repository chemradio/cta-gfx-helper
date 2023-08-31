from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver(driver_url: str) -> webdriver.Remote:
    chrome_options = Options()

    # chrome_options.add_argument("--allow-file-access-from-files")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.headless = True
    # chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("-–disable-gpu")

    device_emulation = {
        "deviceMetrics": {
            "width": 1920,
            "height": 1080,
            "pixelRatio": 1,
        },
    }
    chrome_options.add_experimental_option("mobileEmulation", device_emulation)
    driver = webdriver.Remote(driver_url, options=chrome_options)
    return driver
