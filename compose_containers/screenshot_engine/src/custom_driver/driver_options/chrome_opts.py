from selenium.webdriver.chrome.options import Options

from .user_agent import UserAgent


def _generate_chrome_options(
    dpi_multiplier: int | float,
    user_agent: UserAgent = UserAgent.DESKTOP,
    verical_emulation: bool = True,
    headless: bool = True,
) -> Options:
    chrome_options = Options()
    # chrome_options.add_argument("--incognito")

    chrome_options.add_argument("--window-size=1920,1080")  # just for viewing purposes

    # actual resolution setting
    if verical_emulation:
        chrome_options.add_experimental_option(
            "mobileEmulation",
            {
                "deviceMetrics": {
                    "width": 1920,
                    "height": 5760,
                    "pixelRatio": dpi_multiplier,
                },
                "userAgent": user_agent,
            },
        )

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("-–disable-gpu")

    # to theoretically speed up the process
    if headless:
        chrome_options.add_argument("--headless=new")

    return chrome_options
