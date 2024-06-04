import time

import config
from screenshots.screenshot_capture.capture_single_screenshot import (
    capture_single_screenshot,
)
from screenshots.screenshot_capture.controllers.adblocker.adblocker import Adblocker
from screenshots.screenshot_capture.controllers.auth_controller.auth_controller import (
    BrowserAuthorizer,
)
from screenshots.screenshot_capture.controllers.auth_controller.login_checks import (
    LoginChecker,
)
from screenshots.screenshot_capture.crop_screenshot import crop_screenshot
from screenshots.screenshot_capture.custom_driver.create_driver import create_driver
from screenshots.screenshot_capture.custom_types.screenshot_results import (
    ScreenshotResults,
)
from screenshots.screenshot_capture.custom_types.screenshot_role import ScreenshotRole
from screenshots.screenshot_capture.parse_link_type import parse_link_type
from screenshots.screenshot_capture.routines.screenshot_routines import (
    ScreenshotRoutines,
)


def parse_capture_screenshots(url: str) -> ScreenshotResults:
    clean_url, domain, two_layer = parse_link_type(url)

    # initialize empty screenshots
    foreground_screenshot, background_screenshot = None, None

    # create webdriver
    driver = create_driver(mobile_agent=False, high_resolution=True)

    # prepare driver for LOGIN REQUIRED websites
    if domain in config.LOGIN_REQUIRED:
        BrowserAuthorizer.login_driver_to_domain(driver, domain)
        login_success = LoginChecker.check_domain_login(driver, domain)
        if not login_success:
            raise Exception()

    target_url = clean_url

    # get POST screenshot
    if two_layer:
        driver.get(target_url)
        time.sleep(3)
        try:
            Adblocker.remove_ads(driver)
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
