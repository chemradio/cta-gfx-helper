import time
from dataclasses import astuple
from pathlib import Path

from ..custom_driver import ScreenshotRemoteDriver
from ..helpers.link_parse import parse_link_type
from .capture_single_screenshot import capture_single_screenshot
from .crop_screenshot import crop_screenshot
from .types import ScreenshotResults, ScreenshotRole


def parse_capture_screenshots(
    url: str, remote_driver_url: str, cookie_file_path: Path
) -> ScreenshotResults:
    clean_url, _, two_layer = astuple(parse_link_type(url))

    # initialize empty screenshots
    foreground_screenshot, background_screenshot = None, None

    # create webdriver
    driver = ScreenshotRemoteDriver(
        remote_driver_url=remote_driver_url,
        cookie_file_path=cookie_file_path,
    )

    # prepare driver for LOGIN REQUIRED websites
    driver.login_driver_to_required_domains()

    target_url = clean_url

    # get POST screenshot
    if two_layer:
        driver.get(target_url)
        time.sleep(3)
        try:
            driver.remove_ads()
            time.sleep(1)

            foreground_screenshot = capture_single_screenshot(
                driver, ScreenshotRole.POST
            )
            foreground_screenshot = crop_screenshot(foreground_screenshot)
            profile_url = ScreenshotRoutines.extract_profile_url(driver)
            target_url = profile_url
        except Exception as e:
            print("Social URL is probably for the page, not post:", target_url)
            print("Error encountered: ", str(e))
            two_layer = False
            foreground_screenshot = None

    # get PROFILE / MAIN screenshot
    driver.get(target_url)
    time.sleep(3)

    Adblocker.remove_ads(driver)
    time.sleep(1)

    background_screenshot = capture_single_screenshot(driver, ScreenshotRole.FULL_SIZE)
    background_screenshot = crop_screenshot(background_screenshot)

    driver.quit()

    return ScreenshotResults(
        foreground=foreground_screenshot,
        background=background_screenshot,
        success=True,
        two_layer=two_layer,
    )
