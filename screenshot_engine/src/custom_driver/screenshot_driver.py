from driver_options.user_agent import UserAgent
from selenium import webdriver

from .driver_options.chrome_opts import _generate_chrome_options


def create_remote_driver(
    remote_selenium_url: str, dpi_multiplier: int | float
) -> webdriver.Remote:
    chrome_options = _generate_chrome_options(dpi_multiplier, UserAgent.DESKTOP)
    driver = webdriver.Remote(
        command_executor=remote_selenium_url, options=chrome_options
    )
    return driver
