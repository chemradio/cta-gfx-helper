from selenium import webdriver

from .driver_options.chrome_opts import _generate_chrome_options
from .driver_options.user_agent import UserAgent


def create_remote_driver(
    remote_selenium_url: str,
    dpi_multiplier: int | float,
    vertical_emulation: bool = True,
    headless: bool = True,
) -> webdriver.Remote:
    chrome_options = _generate_chrome_options(
        dpi_multiplier, UserAgent.DOCKER_SELENIUM, vertical_emulation, headless
    )
    driver = webdriver.Remote(
        command_executor=remote_selenium_url, options=chrome_options
    )
    return driver
