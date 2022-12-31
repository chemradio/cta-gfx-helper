import base64
import json
import time
import traceback
from io import BytesIO
from pathlib import Path

from PIL import Image

import config

Image.MAX_IMAGE_PIXELS = 933_120_000
TWO_LAYER_SITES = ("facebook", "instagram", "twitter", "telegram")

from screenshots.browser_authorizer import BrowserAuthorizer
from screenshots.screenshot_routines import ScreenshotRoutines
from screenshots.screenshot_webdriver import ScreenshotWebdriver


class Screenshooter:
    def __init__(self) -> None:
        self.routines = ScreenshotRoutines()
        self.dpi_multiplier = config.DPI_MULTIPLIER
        self.browser_authorizer = BrowserAuthorizer()

    def create_driver(self, mobile: bool = True) -> ScreenshotWebdriver:
        scwd = ScreenshotWebdriver(mobile=mobile)
        return scwd

    def capture_screenshot(self, url, bg_path: Path, fg_path: Path):
        link_type, clean_url, _domain = self.routines.parse_url(url)

        if link_type in config.LOGIN_REQUIRED and config.logged_in_to_social_websites:
            logged_in = True
        else:
            logged_in = False

        mobile = False  # if link_type == 'twitter' else True

        is_two_layer = False if link_type == "scroll" else True
        workflow = self.routines.create_workflow(link_type)

        # create driver
        self.scwd = self.create_driver(mobile=mobile)
        self.driver = self.scwd.driver

        try:
            # authenticate using cookies if required
            if link_type in config.LOGIN_REQUIRED:
                self.browser_authorizer.login_driver_to_domain(
                    driver=self.driver, domain=link_type
                )

            # get post screenshot
            if link_type in TWO_LAYER_SITES:
                self.driver.get(clean_url)
                self.scwd.remove_ads()

                try:
                    self.driver.execute_script("window.stop();")
                    post = workflow.post_routine(url, self.driver, logged_in=logged_in)
                    self._capture_post_screenshot(post, fg_path)

                    link_to_profile = self.routines.extract_profile_url(
                        link_type, url, self.driver, post
                    )
                except:
                    print("Social URL is probably for the page, not post:", clean_url)
                    link_to_profile = clean_url
                    is_two_layer = False
                    link_type = "scroll"

            else:
                link_to_profile = clean_url
                fg_path = ""

            # get profile / main screenshot
            self.driver.get(link_to_profile)
            self.scwd.remove_ads()
            workflow.profile_routine(driver=self.driver)
            self._capture_profile_page_screenshot(bg_path)

            # dump updated cookies if required
            if link_type in config.LOGIN_REQUIRED:
                while True:
                    domain_cookies = self.driver.get_cookies()
                    if len(domain_cookies) < 5:
                        time.sleep(2)
                        continue
                    else:
                        break
                self.scwd.cookie_manager.dump_domain_cookies(link_type, domain_cookies)
            self.driver.quit()

            return True
        except Exception as e:
            print("weirdness")
            self.driver.quit()
            print(e)
            traceback.print_exc()
            raise e

    def _capture_post_screenshot(self, post, fg_path: Path):
        time.sleep(2)
        location = post.location
        size = post.size

        full_post_screenshot = self.driver.command_executor._request(
            "POST",
            self.driver.command_executor._url
            + f"/session/{self.driver.session_id}/chromium/send_command_and_get_result",
            json.dumps(
                {
                    "cmd": "Page.captureScreenshot",
                    "params": {"format": "png", "captureBeyondViewport": False},
                }
            ),
        )["value"]

        im = Image.open(BytesIO(base64.urlsafe_b64decode(full_post_screenshot["data"])))

        # must multiply by zoom or dpi multiplier
        left = location["x"] * self.dpi_multiplier
        top = location["y"] * self.dpi_multiplier
        right = (location["x"] + size["width"]) * self.dpi_multiplier
        bottom = (location["y"] + size["height"]) * self.dpi_multiplier

        im = im.crop((left, top, right, bottom))
        im = im.crop((0, 0, im.width, min(5000, im.height)))
        im.save(str(fg_path))
        return True

    def _capture_profile_page_screenshot(self, bg_path: Path):
        try:
            time.sleep(5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            self.driver.execute_script(
                "window.scrollTo(0, -document.body.scrollHeight)"
            )
            time.sleep(3)

            page_rect = self.driver.command_executor._request(
                "POST",
                self.driver.command_executor._url
                + f"/session/{self.driver.session_id}/chromium/send_command_and_get_result",
                json.dumps({"cmd": "Page.getLayoutMetrics", "params": {}}),
            )

            # page_rect = self.driver.execute_cdp_cmd("Page.getLayoutMetrics", {})

            target_height = (
                5000
                if page_rect["value"]["contentSize"]["height"] > 5000
                else page_rect["value"]["contentSize"]["height"]
            )

            full_page_screenshot = self.driver.command_executor._request(
                "POST",
                self.driver.command_executor._url
                + f"/session/{self.driver.session_id}/chromium/send_command_and_get_result",
                json.dumps(
                    {
                        "cmd": "Page.captureScreenshot",
                        "params": {"format": "png", "captureBeyondViewport": False},
                    }
                ),
            )["value"]

            im = Image.open(
                BytesIO(base64.urlsafe_b64decode(full_page_screenshot["data"]))
            )
            im = im.crop((0, 0, im.width, min(7000, im.height)))

            im.save(str(bg_path))

        except:
            # make some new exceptions
            pass
