import time
from dataclasses import astuple
from pathlib import Path

from ..custom_driver.screenshot_driver import create_remote_driver
from ..helpers.adblock.adblocking import remove_ads
from ..helpers.driver_auth import authenticate_driver
from ..helpers.link_parse import parse_link_type
from .page_routines import apply_routine, extract_profile_url
from .screenshor_capture.capture_screenshot import capture_single_screenshot
from .screenshor_capture.crop_screenshot import crop_screenshot
from .types import ScreenshotResults, ScreenshotRole


def parse_capture_screenshots(
    url: str,
    remote_driver_url: str,
    cookie_file_path: Path,
    dpi_multiplier: int | float,
) -> ScreenshotResults:
    clean_url, domain, two_layer = astuple(parse_link_type(url))

    # initialize empty screenshots
    foreground_screenshot, background_screenshot = None, None

    # create webdriver
    driver = create_remote_driver(remote_driver_url, dpi_multiplier)

    target_url = clean_url

    # login to required sites
    authenticate_driver(driver, domain, cookie_file_path)

    # navigate to POST screenshot
    if two_layer:
        driver.get(target_url)
        time.sleep(3)  # wait for page js to load
        try:
            remove_ads(driver)
            time.sleep(1)  # wait for ads to be removed due to js glitches

            # apply routine
            target_element = apply_routine(driver, ScreenshotRole.POST, domain)

            foreground_screenshot = capture_single_screenshot(
                driver, target_element, ScreenshotRole.POST
            )
            foreground_screenshot = crop_screenshot(
                foreground_screenshot, dpi_multiplier
            )
            profile_url = extract_profile_url(driver, domain)
            target_url = profile_url
        except Exception as e:
            print("Social URL is probably for the page, not post:", target_url)
            print("Error encountered: ", str(e))
            two_layer = False
            foreground_screenshot = None

    # navigate to PROFILE / MAIN screenshot
    driver.get(target_url)
    time.sleep(3)  # wait for page js to load

    remove_ads(driver)
    time.sleep(1)  # wait for ads to be removed due to js glitches

    # apply routine
    target_element = apply_routine(driver, ScreenshotRole.FULL_SIZE, domain)

    background_screenshot = capture_single_screenshot(
        driver, target_element, ScreenshotRole.FULL_SIZE
    )
    background_screenshot = crop_screenshot(background_screenshot, dpi_multiplier)

    driver.quit()

    return ScreenshotResults(
        foreground=foreground_screenshot,
        background=background_screenshot,
        success=True,
        two_layer=two_layer,
    )
