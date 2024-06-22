from selenium.webdriver.chrome.options import Options

import config

from .user_agent import UserAgent


def _generate_chrome_options(user_agent: UserAgent = UserAgent.DESKTOP) -> Options:
    chrome_options = Options()
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    chrome_options.add_argument("--window-size=1920,1080")  # just for viewing purposes

    # actual resolution setting
    chrome_options.add_experimental_option(
        "mobileEmulation",
        {
            "deviceMetrics": {
                "width": 1920,
                "height": 5760,
                "pixelRatio": config.DPI_MULTIPLIER,
            },
            "userAgent": user_agent,
        },
    )

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("-–disable-gpu")

    # to theoretically speed up the process
    chrome_options.headless = True

    return chrome_options
