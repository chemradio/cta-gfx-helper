import json
import os
import time

from selenium import webdriver

import config


class CookieManager:
    """Cookie managing. Store and load saved cookies to the driver"""

    def __init__(self):
        self.cookie_file = config.COOKIE_FILE
        self.initialize_cookie_storage()
        # self.clean_expired_cookies()

    def initialize_cookie_storage(self) -> None:
        """Create cookie file json if does not exist already."""
        if not self.cookie_file.exists():
            with open(self.cookie_file, "a+") as cookie_file:
                json.dump({"domain_name": [{}]}, cookie_file)

    def get_stored_cookies(self) -> dict[list[dict]]:
        """Read all cookies from storage."""
        cookies = dict()
        with open(f"{self.cookie_file}", "r") as cookie_file:
            cookies = json.load(cookie_file)
        return cookies

    def dump_domain_cookies(self, domain: str, domain_cookies: list[dict]) -> None:
        """Save specific domain cookies to storage."""
        stored_cookies = self.get_stored_cookies()
        stored_cookies[domain] = domain_cookies
        with open(f"{self.cookie_file}", "w") as cookie_file:
            json.dump(stored_cookies, cookie_file)

    def add_domain_cookies(self, domain: str, driver: webdriver.Chrome) -> None:
        """Add specific domain cookies to webdriver. Add try/except block around this method - KeyError is possible."""
        domain_cookies = self.get_stored_cookies()[domain]

        good_cookies = 0
        failed_cookies = 0
        for cookie in domain_cookies:
            try:
                driver.add_cookie(cookie)
                good_cookies += 1
                print(
                    f"Successfully loaded cookies: {good_cookies}/{len(domain_cookies)}"
                )
            except:
                failed_cookies += 1
                print(f"Failed to load cookies: {failed_cookies}/{len(domain_cookies)}")

    def clean_expired_cookies(self) -> None:
        """Unused method to clean expired cookies. Not sure if this is necessary at all..."""
        cookies = self.get_stored_cookies()
        for domain, cookie_list in cookies.items():
            clean_cookie_list = list()

            for cookie in cookie_list:
                expiry_time = cookie.get("expiry")
                if expiry_time is not None:
                    if int(time.time()) < int(expiry_time):
                        clean_cookie_list.append(cookie)
            cookies[domain] = clean_cookie_list
        self.force_dump_cookies_dict(cookies)
        return

    def _force_dump_cookies_dict(self, cookies: dict = {}) -> None:
        with open(f"{self.cookie_file}", "w") as cookie_file:
            json.dump(cookies, cookie_file)
        return
