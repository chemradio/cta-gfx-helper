import time
from dataclasses import astuple
from pathlib import Path

from py_gfxhelper_lib.custom_types import ScreenshotRole, ScreenshotResults
from .screenshor_capture.capture_screenshot import capture_crop_single_screenshot
from ..custom_driver import create_remote_driver
from ..link_parse.link_parser import parse_link_type
from ..driver_auth import authenticate_driver
from ..adblock.adblocking import generate_adblock_js_script
from ..page_routines.routine_applicator import (
    apply_post_routine,
    apply_profile_routine,
    extract_profile_url,
)


def parse_capture_screenshots(
    url: str,
    remote_driver_url: str,
    cookie_file_path: Path,
    dpi_multiplier: int | float,
) -> ScreenshotResults:
    error_message = ""
    clean_url, domain, two_layer = astuple(parse_link_type(url))
    foreground_screenshot, background_screenshot = None, None
    driver = create_remote_driver(remote_driver_url, dpi_multiplier)
    target_url = clean_url

    # try to auth the driver. if fails - try to proceed without auth
    auth_success = authenticate_driver(driver, domain, cookie_file_path)
    if not auth_success:
        error_message = "Failed to authenticate driver"

    # navigate to POST screenshot
    if two_layer:
        driver.get(target_url)
        time.sleep(3)
        try:
            driver.execute_script(generate_adblock_js_script())
            time.sleep(1)  # wait for ads to be removed due to js glitches

            target_element = apply_post_routine(driver, domain)
            foreground_screenshot = capture_crop_single_screenshot(
                driver, target_element, ScreenshotRole.POST, dpi_multiplier
            )

            profile_url = extract_profile_url(driver, domain)
            target_url = profile_url
        except Exception as e:
            print("Social URL is probably for the page, not post:", target_url)
            print("Error encountered: ", str(e))
            two_layer = False
            foreground_screenshot = None

    driver.get(target_url)
    time.sleep(3)

    driver.execute_script(generate_adblock_js_script())
    time.sleep(1)

    target_element = apply_profile_routine(driver, domain)
    background_screenshot = capture_crop_single_screenshot(
        driver, target_element, ScreenshotRole.FULL_SIZE, dpi_multiplier
    )

    driver.quit()

    return ScreenshotResults(
        foreground=foreground_screenshot,
        background=background_screenshot,
        success=True,
        two_layer=two_layer,
        error_message=error_message,
    )
