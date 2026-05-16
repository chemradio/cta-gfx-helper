"""Playwright counterpart of ``screenshooter.parse_capture_screenshots``.

Identical capture logic to the Selenium backend - authenticate, optionally
grab the post (foreground) layer, then grab the profile/full-page
(background) layer - but driven by an in-container headless Chromium instead
of a remote Selenium node. No ``remote_driver_url`` is needed.

Used when ``config.SCREENSHOT_BACKEND == "playwright"``.
"""

from dataclasses import astuple
from pathlib import Path

from py_gfxhelper_lib.custom_types import ScreenshotRole, ScreenshotResults

from .screenshor_capture.capture_screenshot_playwright import (
    capture_crop_single_screenshot,
)
from ..custom_driver import playwright_page
from ..link_parse.link_parser import parse_link_type
from ..driver_auth import authenticate_page
from ..adblock.adblocking import generate_adblock_js_script
from ..page_routines.playwright_routine_applicator import (
    apply_post_routine,
    apply_profile_routine,
    extract_profile_url,
    apply_misc_scripts,
)


def parse_capture_screenshots(
    url: str,
    cookie_file_path: Path,
    dpi_multiplier: int | float,
) -> ScreenshotResults:
    error_message = ""
    clean_url, domain, two_layer = astuple(parse_link_type(url))
    foreground_screenshot, background_screenshot = None, None
    target_url = clean_url

    with playwright_page(dpi_multiplier) as (page, context, cdp_session):
        # try to auth the page. if it fails - proceed without auth
        auth_success = authenticate_page(page, context, domain, cookie_file_path)
        if not auth_success:
            error_message = "Failed to authenticate driver"

        # navigate to POST screenshot
        if two_layer:
            page.goto(target_url)
            page.wait_for_timeout(3000)
            try:
                page.wait_for_timeout(1000)  # let ads settle

                # remove "site wants to show notifications" popup
                if domain not in ["facebook"]:
                    page.keyboard.press("Escape")

                apply_misc_scripts(page, ["curseWordObfuscator"])
                target_element = apply_post_routine(page, domain)
                foreground_screenshot = capture_crop_single_screenshot(
                    page,
                    cdp_session,
                    target_element,
                    ScreenshotRole.POST,
                    dpi_multiplier,
                )

                profile_url = extract_profile_url(page, domain)
                target_url = profile_url
            except Exception as e:
                print("Social URL is probably for the page, not post:", target_url)
                print("Error encountered: ", str(e))
                two_layer = False
                foreground_screenshot = None

        page.goto(target_url)
        page.wait_for_timeout(3000)
        # remove "site wants to show notifications" popup
        page.keyboard.press("Escape")

        page.evaluate(f"() => {{ {generate_adblock_js_script()} }}")
        page.wait_for_timeout(1000)

        apply_misc_scripts(page, ["curseWordObfuscator"])

        target_element = apply_profile_routine(page, domain)
        if not target_element:
            target_element = page.query_selector("body")
        background_screenshot = capture_crop_single_screenshot(
            page,
            cdp_session,
            target_element,
            ScreenshotRole.FULL_SIZE,
            dpi_multiplier,
        )

    return ScreenshotResults(
        foreground=foreground_screenshot,
        background=background_screenshot,
        success=True,
        two_layer=two_layer,
        error_message=error_message,
    )
