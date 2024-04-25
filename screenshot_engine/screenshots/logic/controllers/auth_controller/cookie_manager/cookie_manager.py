import json
import time

from selenium import webdriver

import config
from screenshots.logic.controllers.auth_controller.exceptions.cookie_load import (
    CookieLoadException,
)
from screenshots.logic.controllers.auth_controller.exceptions.cookie_missing import (
    MissingCookies,
)


class CookieManager:
    """Cookie managing. Store and load saved cookies to the driver"""

    @staticmethod
    def initialize_cookie_storage() -> None:
        """Create cookie file json if does not exist already."""
        if not config.COOKIE_FILE.exists():
            with open(config.COOKIE_FILE, "w+") as cookie_file:
                json.dump({"domain_name": [{}]}, cookie_file)

    @staticmethod
    def get_stored_cookies() -> dict[list[dict]]:
        """Read all cookies from stored cookie file."""
        cookies = dict()
        with open(config.COOKIE_FILE, "r") as cookie_file:
            cookies = json.load(cookie_file)
        return cookies

    @classmethod
    def dump_domain_cookies(cls, domain: str, domain_cookies: list[dict]) -> None:
        """Save specific domain cookies to storage."""
        stored_cookies = cls.get_stored_cookies()
        stored_cookies[domain] = domain_cookies
        with open(config.COOKIE_FILE, "w") as cookie_file:
            json.dump(stored_cookies, cookie_file)

    @classmethod
    def add_cookies_driver(
        cls, domain: str, driver: webdriver.Chrome | webdriver.Remote
    ) -> None:
        """Add specific domain cookies to webdriver."""
        domain_cookies = cls.get_stored_cookies().get(domain)
        if not domain_cookies:
            raise MissingCookies(domain=domain)

        good_cookies, failed_cookies = 0, 0
        for cookie in domain_cookies:
            try:
                driver.add_cookie(cookie)
                good_cookies += 1
            except:
                failed_cookies += 1

        print(f"Successfully loaded cookies: {good_cookies}/{len(domain_cookies)}")
        print(f"Failed cookies: {failed_cookies}/{len(domain_cookies)}")

        if good_cookies == 0:
            raise CookieLoadException(domain=domain, failed_cookies=failed_cookies)

    @classmethod
    def clean_expired_cookies(cls) -> None:
        """Unused method to clean expired cookies. Not sure if this is necessary at all..."""
        cookies = cls.get_stored_cookies()
        for domain, cookie_list in cookies.items():
            clean_cookie_list = list()

            for cookie in cookie_list:
                expiry_time = cookie.get("expiry")
                if expiry_time is not None:
                    if int(time.time()) < int(expiry_time):
                        clean_cookie_list.append(cookie)
            cookies[domain] = clean_cookie_list
        cls._force_dump_cookies_dict(cookies)

    @staticmethod
    def _force_dump_cookies_dict(cookies: dict = {}) -> None:
        with open(config.COOKIE_FILE, "w") as cookie_file:
            json.dump(cookies, cookie_file)


CookieManager.initialize_cookie_storage()