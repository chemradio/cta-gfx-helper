import json
import os
from pathlib import Path

from selenium import webdriver


class CookieManager:
    """Cookie managing. Store and load saved cookies to the driver"""

    def __init__(self, cookie_file_path: Path):
        self.cookie_file = cookie_file_path
        self.initialize_cookie_storage()

    def initialize_cookie_storage(self) -> None:
        """Create cookie file json if does not exist already."""
        if not os.path.exists(self.cookie_file):
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
        print("Dumping cookies to file")
        stored_cookies = self.get_stored_cookies()
        stored_cookies[domain] = domain_cookies
        with open(f"{self.cookie_file}", "w") as cookie_file:
            json.dump(stored_cookies, cookie_file)

    def add_domain_cookies(self, domain: str, driver: webdriver.Chrome) -> None:
        """Add specific domain cookies to webdriver."""
        domain_cookies = self.get_stored_cookies().get(domain)
        if not domain_cookies:
            print(f"No stored cookies available for domain: {domain}")
            return None

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
