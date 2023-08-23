import time

import config
from screenshots.logic.capture_process.capture_process import capture_screenshot
from screenshots.logic.controllers.adblocker.adblocker import Adblocker
from screenshots.logic.controllers.auth_controller.auth_controller import (
    BrowserAuthorizer,
)
from screenshots.logic.controllers.auth_controller.login_checks import LoginChecker
from screenshots.logic.controllers.routines.screenshot_routines import (
    ScreenshotRoutines,
)
from screenshots.logic.custom_driver.create_driver import create_driver
from screenshots.logic.helpers.crop_screenshot import crop_screenshot
from screenshots.logic.helpers.parse_link_type import parse_link_type
from screenshots.logic.type_classes.screenshot import Screenshot, ScreenshotResults
from screenshots.logic.type_classes.screenshot_role import ScreenshotRole


def capture_screenshots(order: dict) -> ScreenshotResults:
    match order.get("request_type"):
        case "video_files":
            original_url = order.get("background_link")
            clean_url, domain, _ = parse_link_type(original_url)
            two_layer = False
        case _:
            original_url = order.get("link")
            clean_url, domain, two_layer = parse_link_type(original_url)

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
            foreground_screenshot = capture_screenshot(
                driver, ScreenshotRole.POST, order.get("foreground_name")
            )
            foreground_screenshot = crop_screenshot(foreground_screenshot)
            profile_url = ScreenshotRoutines.extract_profile_url(driver)
            target_url = profile_url
        except:
            print("Social URL is probably for the page, not post:", target_url)
            two_layer = False
            foreground_screenshot = None

    # get PROFILE / MAIN screenshot
    driver.get(target_url)
    time.sleep(3)

    background_screenshot = capture_screenshot(
        driver, ScreenshotRole.FULL_SIZE, order.get("background_name")
    )
    background_screenshot = crop_screenshot(background_screenshot)

    driver.quit()

    return ScreenshotResults(
        foreground=foreground_screenshot,
        background=background_screenshot,
        success=True,
        two_layer=two_layer,
    )
