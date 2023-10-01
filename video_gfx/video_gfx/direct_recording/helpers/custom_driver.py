import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver() -> webdriver.Chrome | webdriver.Remote:
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--start-fullscreen")
    chrome_options.add_argument("--kiosk")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--force-frame-rate=25")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("-–disable-gpu")

    # chrome_options.headless = True
    driver = webdriver.Remote(
        config.SELENIUM_CONTAINER,
        options=chrome_options,
    )

    driver.implicitly_wait(5)
    return driver
