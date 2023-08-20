import os
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import config


@dataclass
class UserAgent:
    DESKTOP = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    MOBILE = "userAgent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1"


def create_driver(
    mobile_agent: bool = False,
    high_resolution: bool = True,
) -> webdriver.Chrome | webdriver.Remote:
    user_agent = UserAgent.MOBILE if mobile_agent else UserAgent.DESKTOP

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    if high_resolution:
        chrome_options.add_experimental_option(
            "mobileEmulation",
            {
                "deviceMetrics": {
                    "width": config.SCREENSHOT_DIMENSIONS[0],
                    "height": config.SCREENSHOT_DIMENSIONS[1],
                    "pixelRatio": config.DPI_MULTIPLIER,
                },
                "userAgent": user_agent,
            },
        )

    if config.IS_DOCKER:
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("-–disable-gpu")
        chrome_options.headless = True
        driver = webdriver.Remote(
            config.REMOTE_SCREENSHOT_DRIVER_URL,
            options=chrome_options,
        )
    else:
        driver = webdriver.Chrome(
            executable_path=os.getenv("CHROMEDRIVER_EXECUTABLE"),
            # service=Service(ChromeDriverManager().install()),
            options=chrome_options,
        )

    driver.implicitly_wait(5)
    return driver
