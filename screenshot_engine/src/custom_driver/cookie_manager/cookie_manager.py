import json
from pathlib import Path

from selenium import webdriver


class MissingCookies(Exception):
    def __init__(self, domain):
        self.domain = domain

    def __str__(self):
        return f"No cookies are available for the domain: {self.domain}"


class CookieLoadException(Exception):
    def __init__(self, domain: str, failed_cookies: int):
        self.domain = domain
        self.failed_cookies = failed_cookies

    def __str__(self):
        return f"Failed to load {self.failed_cookies} cookies for domain {self.domain}"


class CookieManager:
    """Cookie managing. Store and load saved cookies to the driver"""

    def __init__(self, cookie_file_path: Path):
        self.COOKIE_FILE = cookie_file_path
        self.initialize_cookie_storage()

    def initialize_cookie_storage(self) -> None:
        """Create cookie file json if does not exist already."""
        if not self.COOKIE_FILE.exists():
            with open(self.COOKIE_FILE, "w+") as cookie_file:
                json.dump({"domain_name": [{}]}, cookie_file)

    def get_stored_cookies(self) -> dict[list[dict]]:
        """Read all cookies from stored cookie file."""
        cookies = dict()
        with open(self.COOKIE_FILE, "r") as cookie_file:
            cookies = json.load(cookie_file)
        return cookies

    def dump_domain_cookies(self, domain: str, domain_cookies: list[dict]) -> None:
        """Save specific domain cookies to storage."""
        stored_cookies = self.get_stored_cookies()
        stored_cookies[domain] = domain_cookies
        with open(self.COOKIE_FILE, "w") as cookie_file:
            json.dump(stored_cookies, cookie_file)

    def add_cookies_driver(
        self, domain: str, driver: webdriver.Chrome | webdriver.Remote
    ) -> None:
        """Add specific domain cookies to webdriver."""
        domain_cookies = self.get_stored_cookies().get(domain)
        if not domain_cookies:
            raise MissingCookies(domain=domain)

        good_cookies, failed_cookies = 0, 0
        for cookie in domain_cookies:
            try:
                driver.add_cookie(cookie)
                good_cookies += 1
            except Exception as e:
                print(f"Failed to load cookie: {cookie} with error: {e[:10]}")
                failed_cookies += 1

        print(f"Successfully loaded cookies: {good_cookies}/{len(domain_cookies)}")
        print(f"Failed cookies: {failed_cookies}/{len(domain_cookies)}")

        if good_cookies == 0:
            raise CookieLoadException(domain=domain, failed_cookies=failed_cookies)
