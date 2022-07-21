import interlinks
import time
import secrets
import base64
import os
from io import BytesIO

from PIL import Image
Image.MAX_IMAGE_PIXELS = 933_120_000
TWO_LAYER_SITES = ('facebook', 'instagram', 'twitter', 'telegram')

from engines.screenshots.screenshot_routines import ScreenshotRoutines
from engines.screenshots.screenshot_webdriver import ScreenshotWebdriver
from engines.screenshots.browser_authorizer import BrowserAuthorizer


from database.db import db_handler
from engines.video_gfx_engines import render_video_orders
from engines.sender_engine import send_ready_orders
from telegram import ReplyKeyboardRemove
from selenium import webdriver

class Screenshooter:
    def __init__(self) -> None:
        self.routines = ScreenshotRoutines()
        self.dpi_multiplier = interlinks.DPI_MULTIPLIER
        self.browser_authorizer = BrowserAuthorizer()
        # self.scwd = ScreenshotWebdriver()
        # self.driver = self.scwd.driver


    def create_driver(self) -> ScreenshotWebdriver:
        scwd = ScreenshotWebdriver()
        return scwd


    def capture_screenshot(self, url):
        link_type, clean_url, domain = self.routines.parse_url(url)

        # generate file names
        background_name = f"01_BG_{secrets.token_hex(8)}.png"
        foreground_name = f"02_FG_{secrets.token_hex(8)}.png"

        is_two_layer = False if link_type == 'scroll' else True
        workflow = self.routines.create_workflow(link_type)

        # create driver
        self.scwd = self.create_driver()
        self.driver = self.scwd.driver

        # authenticate using cookies if required
        if link_type in interlinks.LOGIN_REQUIRED:
            self.browser_authorizer.login_driver_to_domain(driver=self.driver, domain=link_type)
            

        # get post screenshot
        if link_type in TWO_LAYER_SITES:
            self.driver.get(clean_url)
            post = workflow.post_routine(url, self.driver)
            self.driver.execute_script("window.stop();")
            self._capture_post_screenshot(post, foreground_name)
            link_to_profile = self.routines.extract_profile_url(link_type, url, self.driver, post)
        else:
            link_to_profile = clean_url

        # get profile / main screenshot
        self.driver.get(link_to_profile)
        workflow.profile_routine(driver=self.driver)
        self._capture_profile_page_screenshot(background_name)

        # dump updated cookies if required
        if link_type in interlinks.LOGIN_REQUIRED:
            while True:
                domain_cookies = self.driver.get_cookies()
                if len(domain_cookies) < 5:
                    time.sleep(2)
                    continue
                else:
                    break
            self.scwd.cookie_manager.dump_domain_cookies(link_type, domain_cookies)
        self.driver.quit()

        # generate screenshot dict for return
        return {
            "is_two_layer": is_two_layer,
            "bg_path": interlinks.screenshot_folder + "/" + background_name,
            "fg_path": interlinks.screenshot_folder + "/" + foreground_name
            if is_two_layer
            else None,
            "link_type": "instagram" if link_type == "telegram" else link_type,
        }


    def _capture_post_screenshot(self, post, foreground_name):
        # try:
        # self.driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
        time.sleep(2)
        location = post.location
        size = post.size

        page_rect = self.driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
        print(f'{page_rect=}')

        # # not working for some twitter posts
        # full_post_screenshot = self.driver.execute_cdp_cmd(
        #     "Page.captureScreenshot",
        #     {
        #         "fromSurface": True,
        #         "format": "png",
        #         "captureBeyondViewport": True,
        #         "clip": {
        #             "width": page_rect["contentSize"]["width"],
        #             "height": page_rect["contentSize"]["height"],
        #             "x": 0,
        #             "y": 0,
        #             "scale": 1,
        #         },
        #     },
        # )

        full_post_screenshot = self.driver.execute_cdp_cmd(
            "Page.captureScreenshot",
            {
                "format": "png",
                "captureBeyondViewport": False,
            },
        )

        im = Image.open(BytesIO(base64.urlsafe_b64decode(full_post_screenshot["data"])))

        # must multiply by zoom or dpi multiplier
        left = location["x"] * self.dpi_multiplier
        top = location["y"] * self.dpi_multiplier
        right = (location["x"] + size["width"]) * self.dpi_multiplier
        bottom = (location["y"] + size["height"]) * self.dpi_multiplier

        im = im.crop((left, top, right, bottom))
        im = im.crop((0,0, im.width, min(5000,im.height)))
        im.save(f"{interlinks.screenshot_folder}/{foreground_name}")
        return True
        # except:
        #     # make exceptions
        #     print('error!!')
        #     pass


    def _capture_profile_page_screenshot(self, background_name):
        try:
            time.sleep(5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
            time.sleep(3)

            page_rect = self.driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
            target_height = (
                5000
                if page_rect["contentSize"]["height"] > 5000
                else page_rect["contentSize"]["height"]
            )


            # full_page_screenshot = self.driver.execute_cdp_cmd(
            #     "Page.captureScreenshot",
            #     {
            #         "format": "png",
            #         "captureBeyondViewport": False,
            #         "clip": {
            #             "width": page_rect["contentSize"]["width"] / self.dpi_multiplier,
            #             "height": target_height,
            #             "x": 0,
            #             "y": 0,
            #             "scale": 1,
            #         },
            #     },
            # )

            full_page_screenshot = self.driver.execute_cdp_cmd(
                "Page.captureScreenshot",
                {
                    "format": "png",
                    "captureBeyondViewport": False,
                },
            )


            im = Image.open(BytesIO(base64.urlsafe_b64decode(full_page_screenshot["data"])))
            im = im.crop((0,0,im.width, min(7000,im.height)))

            # # must multiply by zoom or dpi multiplier
            # left = location["x"] * self.dpi_multiplier
            # top = location["y"] * self.dpi_multiplier
            # right = (location["x"] + size["width"]) * self.dpi_multiplier
            # bottom = (location["y"] + size["height"]) * self.dpi_multiplier

            # im = im.crop((left, top, right, bottom))
            im.save(f"{interlinks.screenshot_folder}/{background_name}")

            # with open(f"{interlinks.screenshot_folder}/{background_name}", "wb") as file:
            #     file.write(base64.urlsafe_b64decode(full_page_screenshot["data"]))
            # return
        except:
            # make some new exceptions
            pass
