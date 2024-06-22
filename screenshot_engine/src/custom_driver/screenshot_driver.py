from selenium import webdriver

from config import REMOTE_SELENIUM_URL

from .driver_options.chrome_opts import _generate_chrome_options


def create_remote_driver(
    remote_selenium_url: str = REMOTE_SELENIUM_URL,
) -> webdriver.Remote:
    chrome_options = _generate_chrome_options()
    driver = webdriver.Remote(
        command_executor=remote_selenium_url, options=chrome_options
    )
    return driver
